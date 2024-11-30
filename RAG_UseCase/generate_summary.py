from transformers import pipeline
from Logs.Logsconfig import logger
# Load the summarization pipeline or text generation model
summarizer = pipeline("summarization")

# Function to generate a summary based on retrieved reviews
def generate_summary(retrieved_reviews):
    try:
        # Combine retrieved reviews into a single string for context
        context = " ".join(retrieved_reviews)
        
        # Generate summary
        summary = summarizer(context, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logger.error(f"Error during summary generation: {e}")
        return None

