import caiman as cm
from pathlib import Path


def get_temp_movies(
    first_file=None,
    last_file=None,
    step=1,
    downsample_ratio=0.1,
    rigid=False,
    batch_size=3,
):
    path = Path.home() / "caiman_data" / "temp"

    file_identifier = "rig" if rigid else "els"
    filenames = sorted([p for p in path.rglob(f"[!.]?*{file_identifier}*.mmap")])
    filenames = filenames[first_file:last_file:step]

    assert filenames, "No movies found in the caiman temp folder"

    print(f"Processing file: {filenames[0]}")
    movie_chain = cm.load(filenames[0]).resize(1, 1, downsample_ratio)

    for batch in batched(filenames[1:], batch_size):
        batch_movies = [movie_chain]

        for filename in batch:
            print(f"Processing file: {filename}")
            batch_movies.append(cm.load(filename).resize(1, 1, downsample_ratio))

        movie_chain = cm.concatenate(batch_movies, axis=0)

    return movie_chain


def batched(full_list, batch_size):
    for index in range(0, len(full_list), batch_size):
        yield full_list[index : index + batch_size]
