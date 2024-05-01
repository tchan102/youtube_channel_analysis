import pandas as pd
import matplotlib.pyplot as plt

def load_data(filename):
    return pd.read_pickle(filename)

def top_k_videos(df, k):
    return df.sort_values(by='LengthInSeconds', ascending=False).head(k)

def filter_videos_by_length(df, min_length_sec, max_length_sec):
    filtered_df = df[(df['LengthInSeconds'] >= min_length_sec) & (df['LengthInSeconds'] <= max_length_sec)]
    return filtered_df

video_df = load_data('video_data.pkl')
minute = 60

min_length_sec = 0 * minute 
max_length_sec = 20 * minute 

filtered_videos = filter_videos_by_length(video_df, min_length_sec, max_length_sec)
print(filtered_videos)

filtered_videos.to_pickle('filtered_video_data.pkl')

plt.figure(figsize=(10, 6))
plt.hist(filtered_videos['LengthInSeconds'] / 60, bins=20, color='blue', edgecolor='black')
plt.title('Histogram of Video Lengths')
plt.xlabel('Length in Minutes')
plt.ylabel('Number of Videos')
plt.grid(True)
plt.show()