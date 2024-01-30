import psycopg2
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from datetime import datetime
import csv
import yaml

def read_postgresql_config(filename='config.yml', section='postgresql'):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    
    if section in config:
        return config[section]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

def read_video_processing_config(filename='config.yml', section='video_processing'):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    
    if section in config:
        return config[section]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_data (
            clip_name VARCHAR,
            clip_file_extension VARCHAR,
            clip_duration FLOAT,
            clip_location VARCHAR,
            insert_timestamp TIMESTAMP
        );
    """)

def insert_data(conn, data):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO video_data (
            clip_name,
            clip_file_extension,
            clip_duration,
            clip_location,
            insert_timestamp
        ) VALUES (%s, %s, %s, %s, %s);
    """, data)

    conn.commit()
    cursor.close()

def save_to_csv(data, report_folder):
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    csv_file_path = os.path.join(report_folder, 'generated_video_files.csv')

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['clip_name', 'clip_file_extension', 'clip_duration', 'clip_location', 'insert_timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

def cut_video_and_insert_data(input_file, output_folder, report_folder, clip_duration=60):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read configuration from config.yml
    config_db = read_postgresql_config()
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**config_db)

    create_table(conn)

    video_clip = VideoFileClip(input_file)
    total_frames = int(video_clip.fps * video_clip.duration)
    frames_per_clip = int(video_clip.fps * clip_duration)

    csv_data = []

    for start_frame in range(0, total_frames, frames_per_clip):
        end_frame = min(start_frame + frames_per_clip, total_frames)
        subclip = video_clip.subclip(start_frame / video_clip.fps, end_frame / video_clip.fps)

        output_name = f"{start_frame}thFrame.mp4"
        output_path = os.path.join(output_folder, output_name)

        subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        data = (
            os.path.splitext(output_name)[0],
            os.path.splitext(output_name)[1][1:],
            subclip.duration,
            output_path,
            datetime.now()
        )
        insert_data(conn, data)
        csv_data.append(dict(zip(['clip_name', 'clip_file_extension', 'clip_duration', 'clip_location', 'insert_timestamp'], data)))

    # Save data to CSV in the report folder
    save_to_csv(csv_data, report_folder)

    video_clip.close()
    conn.close()

# Excecute the code
if __name__ == "__main__":
    config_video_processing = read_video_processing_config()
    input_file = config_video_processing['input_file']
    output_folder = config_video_processing['output_folder']
    report_folder = config_video_processing['report_folder']
    cut_video_and_insert_data(input_file, output_folder, report_folder)
