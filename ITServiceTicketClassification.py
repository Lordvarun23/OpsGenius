import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# Step 1: Load the dataset
# Assuming your dataset is in a CSV file named 'tickets.csv' with columns 'Document' and 'Topic_group'
data = pd.read_csv('tickets.csv')

# Step 2: Preprocess Data
# Remove any rows with missing values
data = data.dropna(subset=['Document', 'Topic_group'])

# Step 3: Convert Text to Features
# Using TfidfVectorizer to convert text into numerical features
X = data['Document']
y = data['Topic_group']

# Step 4: Split the Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the Model
# Create a pipeline with TfidfVectorizer and MultinomialNB
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('nb', MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

# Step 6: Evaluate the Model
# Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Print classification report and accuracy
print(classification_report(y_test, y_pred))
print('Accuracy:', accuracy_score(y_test, y_pred))

# Save the trained model for later use
import joblib
joblib.dump(pipeline, 'ticket_classifier_model.pkl')

# Example usage:
# loaded_model = joblib.load('ticket_classifier_model.pkl')
# new_tickets = ["Need access to the new project files", "Printer is not working"]
# predictions = loaded_model.predict(new_tickets)
# print(predictions)

