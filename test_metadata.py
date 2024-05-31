import glob
import os
import sys
import yaml
from yaml import SafeLoader
from metadata.metadata import Metadata


def main(metadata_dir):
    """ "
    Test that all current lexicon metadata is parsable by Pydantic model
    (They are not because model falsely assumes that lexicons only have size.entries)
    """
    for filename in glob.glob(os.path.join(metadata_dir, "*yaml")):
        with open(filename) as fp:
            print(filename)
            obj = yaml.load(fp, Loader=SafeLoader)
            # raises exception if it fails
            Metadata.parse_obj(obj)


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        main(path)
    except IndexError:
        print("Usage: python test_metadata.py <path_to_dir_with_lexicon_metadata>")
