import re
import pandas as pd

def load_chat(filename):
    """
    Reads and processes a WhatsApp chat file into a structured Pandas DataFrame.

    Parameters:
        filename (str): Path to the WhatsApp chat text file.

    Returns:
        pd.DataFrame: Processed DataFrame with structured columns.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
        
        pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s?[ap]m\s?-"
        messages = re.split(pattern, data)[1:] 
        dates = re.findall(pattern, data)

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p -', errors='coerce')
        df.rename(columns={'message_date': 'date'}, inplace=True)
        df['user_message'] = df['user_message'].astype(str)
        pattern = r'^([\w\s]+?):\s(.+)$'
        df[['user', 'message']] = df['user_message'].str.extract(pattern, expand=True)

        df.fillna({'user': 'notification'}, inplace=True)
        df.fillna({'message': df['user_message']}, inplace=True)
        df.drop(columns=['user_message'], inplace=True)

        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['year'] = df['date'].dt.year
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute

        return df

    except Exception as e:
        print(f"Error loading chat: {e}")
        return None

