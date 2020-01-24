import os

def process(event):
    # filename (event.src_path)
    filename = os.path.realpath(event.src_path)
    print(event.event_type, event.is_directory, filename)
