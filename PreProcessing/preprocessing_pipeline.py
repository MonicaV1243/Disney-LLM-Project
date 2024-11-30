import PreProcessing.Preprocess as pp
from Logs.Logsconfig import logger

def preprocess(data):
    try:
        logger.info("Preprocessing Task Started")
        remove_cols = pp.remove_unwanted_columns(data)

        handle_null_values = pp.hanlde_null_values(remove_cols)

        normalize_data = pp.normalize_object_columns(handle_null_values)

        ner = pp.extract_named_entities(normalize_data)
        logger.info("Preprocessing Task Completed Successfully")

        return ner
    except Exception as e:
        logger.error("Error Occurred duting Pre Processing :" + str(e))
        return None

