from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import os
import logging
import language_tool_python
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='frontend/dist/assets', template_folder='frontend/dist', static_url_path='/assets')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LT_SERVER_URL = os.environ.get('LT_SERVER_URL') or None
DISABLE_LOCAL_LT = os.environ.get('DISABLE_LOCAL_LT', '1') in ('1', 'true', 'True')
START_LOCAL_LT_BACKGROUND = os.environ.get('START_LOCAL_LT_BACKGROUND', '0') in ('1', 'true', 'True')

tool = None
if LT_SERVER_URL:
    try:
        tool = language_tool_python.LanguageTool(server_url=LT_SERVER_URL)
        logger.info(f"Using remote LanguageTool at {LT_SERVER_URL}")
    except Exception as e:
        logger.warning(f"Failed to connect to remote LanguageTool: {e}")
else:
    if not DISABLE_LOCAL_LT and START_LOCAL_LT_BACKGROUND:
        import threading
        def _init_local_tool():
            global tool
            try:
                tool = language_tool_python.LanguageTool('en-US')
                logger.info("Local LanguageTool initialized")
            except Exception as e:
                logger.warning(f"Local LanguageTool init failed: {e}")
        threading.Thread(target=_init_local_tool, daemon=True).start()

LANGUAGE_MAP = {"French": "fr", "Spanish": "es", "German": "de", "Italian": "it", "Russian": "ru", "Chinese": "zh", "Hindi": "hi"}

def spell_correct(text: str) -> str:
    try:
        blob = TextBlob(text)
        corrected = str(blob.correct())
        if text.lower().startswith("she ") and corrected.lower().startswith("the "):
            corrected = "She" + corrected[3:]
        corrected = corrected.replace("dont", "don't").replace("Dont", "Don't")
        return corrected
    except Exception as e:
        logger.error(f"Spell correction error: {e}")
        return text

def grammar_correct(text: str, original: str = None) -> str:
    try:
        if not tool:
            return text
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        if original and corrected.strip() == text.strip():
            matches = tool.check(original)
            corrected = language_tool_python.utils.correct(original, matches)
        return corrected
    except Exception as e:
        logger.error(f"Grammar correction error: {e}")
        return text

paraphraser = None
def paraphrase_text(text: str) -> str:
    try:
        global paraphraser
        if paraphraser is None:
            from transformers import T5ForConditionalGeneration, T5Tokenizer
            model_name = "Vamsi/T5_Paraphrase_Paws"
            paraphraser = {
                'model': T5ForConditionalGeneration.from_pretrained(model_name),
                'tokenizer': T5Tokenizer.from_pretrained(model_name)
            }
            logger.info("Paraphrase model loaded (220MB)")
        tokenizer, model = paraphraser['tokenizer'], paraphraser['model']
        input_text = f"paraphrase: {text} </s>"
        inputs = tokenizer(input_text, return_tensors="pt", max_length=256, truncation=True)
        outputs = model.generate(inputs.input_ids, max_length=128, num_beams=4, num_return_sequences=1, temperature=1.5)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result if result.strip() else text
    except Exception as e:
        logger.error(f"Paraphrasing error: {e}", exc_info=True)
        return text

humanizer = None
def humanize_text(text: str) -> str:
    try:
        global humanizer
        if humanizer is None:
            from transformers import T5ForConditionalGeneration, T5Tokenizer
            model_name = "Vamsi/T5_Paraphrase_Paws"
            humanizer = {
                'model': T5ForConditionalGeneration.from_pretrained(model_name),
                'tokenizer': T5Tokenizer.from_pretrained(model_name)
            }
            logger.info("Humanizer model loaded (220MB)")
        
        tokenizer, model = humanizer['tokenizer'], humanizer['model']
        input_text = f"paraphrase: {text} </s>"
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate multiple variations
        outputs = model.generate(
            inputs.input_ids,
            max_length=200,
            num_beams=10,
            num_return_sequences=3,
            temperature=1.5,
            top_k=100,
            top_p=0.92,
            do_sample=True,
            early_stopping=False
        )
        
        # Pick the most different result
        results = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        best_result = text
        max_diff = 0
        for result in results:
            if result.strip():
                orig_words = set(text.lower().split())
                result_words = set(result.lower().split())
                diff = len(orig_words.symmetric_difference(result_words))
                if diff > max_diff:
                    max_diff = diff
                    best_result = result
        
        # Add contractions for natural feel
        humanized = best_result
        humanized = humanized.replace(" will not ", " won't ")
        humanized = humanized.replace(" do not ", " don't ")
        humanized = humanized.replace(" does not ", " doesn't ")
        humanized = humanized.replace(" cannot ", " can't ")
        humanized = humanized.replace(" I am ", " I'm ")
        humanized = humanized.replace(" you are ", " you're ")
        humanized = humanized.replace(" it is ", " it's ")
        
        return humanized if humanized.strip() and humanized != text else text
    except Exception as e:
        logger.error(f"Humanization error: {e}", exc_info=True)
        return text

summarizer = None
def summarize_text(text: str) -> str:
    try:
        global summarizer
        if summarizer is None:
            from transformers import pipeline as _pipeline
            summarizer = _pipeline("summarization", model="facebook/bart-large-cnn")
            logger.info("Summarization model loaded (1.63GB - high quality)")
        
        input_length = len(text.split())
        
        if input_length < 100:
            max_len = min(input_length + 20, 150)
            min_len = max(10, input_length // 3)
        else:
            max_len = min(200, max(80, input_length // 2))
            min_len = min(40, max_len - 30)
        
        result = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False, truncation=True)
        
        if isinstance(result, list) and 'summary_text' in result[0]:
            summary = result[0]['summary_text']
            if summary and not summary[-1] in '.!?':
                for punct in ['. ', '! ', '? ']:
                    last_idx = summary.rfind(punct)
                    if last_idx > len(summary) // 2:
                        summary = summary[:last_idx + 1]
                        break
            return summary
        return str(result)
    except Exception as e:
        logger.error(f"Summarization error: {e}", exc_info=True)
        return text

translation_models = {}
def translate_text(text: str, target_lang: str = "fr") -> str:
    try:
        if target_lang not in LANGUAGE_MAP.values():
            return f"Translation not supported. Supported: {', '.join(LANGUAGE_MAP.keys())}"
        model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
        if model_name not in translation_models:
            from transformers import MarianMTModel, MarianTokenizer
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            translation_models[model_name] = {'tokenizer': tokenizer, 'model': model}
            logger.info(f"Translation model loaded: {model_name}")
        tokenizer, model = translation_models[model_name]['tokenizer'], translation_models[model_name]['model']
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        translated = model.generate(**inputs)
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        return output if output.strip().lower() != text.strip().lower() else text
    except Exception as e:
        logger.error(f"Translation error: {e}", exc_info=True)
        return "Translation failed"

def validate_text_input(text: str, max_length: int = 2000) -> tuple[bool, str]:
    if not text:
        return False, "Text input is required"
    if not isinstance(text, str):
        return False, "Text must be a string"
    if len(text) > max_length:
        return False, f"Text exceeds maximum length of {max_length} characters"
    return True, ""

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "languagetool_available": tool is not None}), 200

@app.route("/api/correct", methods=["POST"])
def api_correct():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        text = data.get("text", "").strip()
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        spell_corrected = spell_correct(text)
        grammar_corrected = grammar_correct(spell_corrected, original=text)
        return jsonify({"original": text, "spell_version": spell_corrected, "corrected": grammar_corrected}), 200
    except Exception as e:
        logger.error(f"Correction API error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/paraphrase", methods=["POST"])
def api_paraphrase():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        paraphrased = paraphrase_text(text)
        return jsonify({"original": text, "paraphrased": paraphrased}), 200
    except Exception as e:
        logger.error(f"Paraphrase API error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/humanize", methods=["POST"])
def api_humanize():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        humanized = humanize_text(text)
        return jsonify({"original": text, "humanized": humanized}), 200
    except Exception as e:
        logger.error(f"Humanize API error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        summary = summarize_text(text)
        return jsonify({"original": text, "summary": summary}), 200
    except Exception as e:
        logger.error(f"Summarize API error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/translate", methods=["POST"])
def api_translate():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        target_lang_name = data.get("target_lang", "French")
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        target_lang_code = LANGUAGE_MAP.get(target_lang_name, "fr")
        translated = translate_text(text, target_lang=target_lang_code)
        return jsonify({"original": text, "translated": translated, "target_lang": target_lang_name}), 200
    except Exception as e:
        logger.error(f"Translate API error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return app.send_static_file(path)
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ('true', '1', 'yes')
    if not tool and not LT_SERVER_URL:
        try:
            logger.info("Attempting to start local LanguageTool...")
            tool = language_tool_python.LanguageTool('en-US')
            logger.info("Local LanguageTool started successfully")
        except Exception as e:
            logger.error(f"Failed to start local LanguageTool: {e}")
    logger.info(f"Starting Flask app on port {port}")
    app.run(debug=debug, port=port, host='0.0.0.0')