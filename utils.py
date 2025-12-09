import caiman as cm
from pathlib import Path

def get_temp_movies(
    first_file=None,
    last_file=None,
    step=1,
    downsample_ratio=0.1,
    rigid=False,
):
    path = Path.home() / "caiman_data" / "temp"

    file_identifier = "rig" if rigid else "els"
    filenames = sorted([p for p in path.rglob(f"[!.]?*{file_identifier}*.mmap")])[
        first_file:last_file:step
    ]

    assert filenames, "No movies found in the caiman temp folder"

    print(f"Processing file: {filenames[0]}")
    movie_chain = cm.load(filenames[0]).resize(1, 1, downsample_ratio)
    
    for filename in filenames[1:]:
        print(f"Processing file: {filename}")
        movie = cm.load(filename).resize(1, 1, downsample_ratio)
        movie_chain = cm.concatenate([movie_chain, movie], axis=0)

    
    return movie_chain