import csv
import hashlib
from math import inf
from pathlib import Path
from featureExtractor import featExt

class dsWriter():
    """
    This class is in charge of transforming the original trec0X database into a csv file more suited
    for this project's data model.
    """
    def transformBase(self, base='base/', maxl=inf):
        parent_dir = Path(__file__).parent
        rel_to_formated = "../dataSets/formated/ds.csv"
        path_to_formated = (parent_dir / rel_to_formated).resolve()

        if self._checkBaseIntegrity(path_to_formated):
            return

        rel_to_base = "../dataSets/"+base
        base_indexes = ["trec05p-1/full/index" ,"trec06p/full/index" ,"trec07p/full/index"]
        path_to_base = (parent_dir / rel_to_base).resolve()
        fe = featExt()

        with open(path_to_formated, 'a+') as target_ds:
            writer = csv.DictWriter(target_ds, featExt.keys)
            writer.writeheader()
            for index_path in base_indexes:
                path_to_file = (path_to_base / index_path).resolve()
                with open(path_to_file, 'r') as ifile:
                    for ind, line in enumerate(ifile):
                        if ind > maxl:
                            break
                        cls, rel_path = line.split(' ')
                        path_to_mail = (Path(path_to_file).parent / rel_path[:-1]).resolve()

                        with open(path_to_mail,'r',encoding='iso-8859-15') as mfile:
                            try:
                                writer.writerow(fe.getFeatures(mfile.read(), cls))
                            except Exception as exception:
                                report = 'There has been a problem in file {}: {}, error trace: {}, skipping file'.format(ind, path_to_mail, exception)
                                print(report)
                                continue

    def _checkBaseIntegrity(self, path_to_csv_file):
        digest = "bac9ee467d8e431b94f60095bb5a11ac5f8c3e6cde05339c324d3017ade2e9015a7e59156bd" + \
            "4805c78c73f6c44d0c80dfcec2deeb2a89652a9fc215f9e97c165"

        with open(path_to_csv_file, mode='rb' ) as csvfile:
            h_blake = hashlib.blake2b()
            buf = csvfile.read()
            h_blake.update(buf)
            return h_blake.hexdigest() == digest

        return False
