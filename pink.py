import pandas as pd
import os

def process_file(file_path):
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Filter only Pink Morsels
    df = df[df['product'] == 'pink morsel']
    
    # Calculate sales (price * quantity)
    # First remove $ sign and convert price to float
    df['price'] = df['price'].str.replace('$', '').astype(float)
    df['sales'] = df['price'] * df['quantity']
    
    # Select only required columns
    df = df[['sales', 'date', 'region']]
    
    return df

def main():
    # Get all CSV files in data directory
    data_dir = 'data'
    output_file = 'formatted_output.csv'
    
    all_data = pd.DataFrame()
    
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(data_dir, file)
            processed_data = process_file(file_path)
            all_data = pd.concat([all_data, processed_data])
    
    # Save combined data to new CSV
    all_data.to_csv(output_file, index=False)
    print(f"Formatted data saved to {output_file}")

if __name__ == '__main__':
    main()