from transformers import BartForConditionalGeneration, BartTokenizer
import pymongo

def summarize_assigned_tasks(paragraph):
    # Load pre-trained model and tokenizer
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

    # Tokenize the input paragraph
    inputs = tokenizer.encode("summarize: " + paragraph, return_tensors="pt", max_length=1024, truncation=True)

    # Generate the summary
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

# Example paragraph
#input_paragraph = """Embarking on the development of a nature website, the task is assigned to a skilled team poised to infuse creativity and technical expertise. Comprising talented individuals, the team features Hannah, known for her intuitive design finesse, John, adept in backend development, and Maria, a content wizard with a flair for storytelling. With their collaborative synergy, the website's vision will materialize; Hannah's captivating aesthetics will harmonize with John's robust coding, while Maria's compelling content will breathe life into the platform. Together, this diverse team promises an immersive, informative, and visually stunning nature website, envisioned to inspire and educate visitors."""
input_paragraph = input("Enter your text to summarize: ")

# Get the summary
result_summary = summarize_assigned_tasks(input_paragraph)
#print("Summary of assigned tasks:\n", result_summary)


# Establish a connection to your MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Summary"]  # Replace with your database name
collection = db["Tensorflow"]  # Replace with your collection name

# Your Python code that generates output
output_data = {
    "original text": input_paragraph,
    "summary": result_summary
}

# Insert the output into MongoDB
inserted_data = collection.insert_one(output_data)
print("Output inserted. The object id is:", inserted_data.inserted_id)
