import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.manifold import MDS
from ..models.axelrod_classic import *
from ..models.topographic_variant import *


def _classic_print_as_grid(df):
    _print_as_grid(df, _classic_create_grid)


def _classic_create_grid(df, traits_in_single_dim):
    grid = [[None for _ in range(int(math.sqrt(len(df))))] for _ in range(int(math.sqrt(len(df))))]
    mask = [[False for _ in range(int(math.sqrt(len(df))))] for _ in range(int(math.sqrt(len(df))))]
    for index, row in df.iterrows():
        grid[row[ColumnNames.LOCATION][0]][row[ColumnNames.LOCATION][1]] = traits_in_single_dim[index, 0]
    return grid, mask


def _print_as_grid(df, create_grid):
    # prepare data for dimension reduction
    matrix = np.zeros((len(df), len(df.at[0, ColumnNames.TRAITS])))
    for index, row in df.iterrows():
        matrix[index, :] = row[ColumnNames.TRAITS]

    # reduce dimensionality
    all_rows_in_matrix_are_the_same = np.all(matrix == matrix[0])
    traits_in_single_dim = np.full((len(df), 1), 1)
    if not all_rows_in_matrix_are_the_same:
        mds = MDS(random_state=0, n_components=1)
        traits_in_single_dim = mds.fit_transform(matrix)

    # create grid to print
    grid, mask = create_grid(df, traits_in_single_dim)

    # print as heatmap
    sns.heatmap(data=np.array(grid), mask=np.array(mask))  # cbar=False
    plt.show()


def _show_analyze_by_region(df):
    df["traits_as_str"] = df[ColumnNames.TRAITS].apply(lambda x: str(x))
    analyze_by_region_df = pd.DataFrame()
    analyze_by_region_df["num_of_unique_traits"] = df.groupby(ColumnNames.REGION)["traits_as_str"].nunique()
    analyze_by_region_df["unique_traits"] = df.groupby(ColumnNames.REGION)["traits_as_str"].unique().apply(lambda x: str(x))
    analyze_by_region_df["population_size"] = df.groupby(ColumnNames.REGION).size()
    print(analyze_by_region_df.to_markdown())


def _analyze_polarization_state(df, print_heat_map, model_specific_polarization_state_analyze):
    if print_heat_map is not None:
        print_heat_map(df)
    model_specific_polarization_state_analyze(df)


def classic_analyze_polarization_state(df):
    _analyze_polarization_state(df, print_heat_map=_classic_print_as_grid,
                                model_specific_polarization_state_analyze=lambda x: x)


def topographic_analyze_polarization_state(df):
    _analyze_polarization_state(df, print_heat_map=None,
                                model_specific_polarization_state_analyze=_show_analyze_by_region)
