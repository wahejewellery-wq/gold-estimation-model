import pandas as pd

try:
    df = pd.read_csv('data.csv')
    print(f"Total rows: {len(df)}")
    
    # Filter for Rings
    rings_df = df[df['Product Title'].str.contains('Ring', case=False, na=False)]
    print(f"Rows with 'Ring' in title: {len(rings_df)}")
    
    unique_rings = rings_df['Product Title'].unique()
    print(f"Unique Ring Product Titles: {len(unique_rings)}")
    
    # Check purities
    print("\nPurity distribution in Rings:")
    print(rings_df['Purity'].value_counts())
    
    # Check if 'Variant Title' can be parsed for size
    # Format seems to be "Purity / Color / Size"
    def extract_size(variant_title):
        parts = str(variant_title).split('/')
        if len(parts) >= 3:
            return parts[-1].strip()
        return None

    rings_df['Ring Size'] = rings_df['Variant Title'].apply(extract_size)
    print("\nTop 10 Ring Sizes:")
    print(rings_df['Ring Size'].value_counts().head(10))

    # Check for "767" in any column
    print("\nChecking for '767' value in dataframe:")
    for col in df.columns:
        if df[col].astype(str).str.contains('767').any():
            print(f"Found '767' in column: {col}")
            print(df[df[col].astype(str).str.contains('767')][col].head())

except Exception as e:
    print(f"Error: {e}")
