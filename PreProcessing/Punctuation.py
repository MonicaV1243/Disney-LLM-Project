import yaml
from torch import package
from config import Punctuation_Model, Punctuation_Yml
from Logs.Logsconfig import logger
def add_punctuations(text):
    try:
        with open(Punctuation_Yml, 'r',  encoding='utf-8') as yaml_file:
            models = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        model_path = Punctuation_Model

        imp = package.PackageImporter(model_path)
        model = imp.load_pickle("te_model", "model")

        def apply_te(text, lan='en'):
            return model.enhance_text(text, lan)

        output_text = apply_te(text, lan='en')
        return output_text
    except Exception as e:
        logger.error("Error Occurred when adding punctuation :" + str(e))
        return "Error Occurred :" + str(e)

