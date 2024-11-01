import pandas as pd

data = [
    "Pathway is a real-time data processing framework that enables developers to build robust data pipelines.",
    "It excels in handling streaming data and provides powerful capabilities for building real-time AI applications.",
    "Some key features of Pathway include: Real-time data processing, Built-in support for AI/ML workflows"
]

# Create DataFrame
df = pd.DataFrame(data, columns=['content'])

# Save as CSV
df.to_csv('data/documents.csv', index=False, quoting=1) 