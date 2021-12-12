from util import *

polarization_metrics_classic, final_df_classic = run_axelrod(
    display_name="Classic"
)
polarization_metrics_single_region, final_df_single_region = run_axelrod(
    display_name="Single Region",
    passive_selection=select_passive_by_region,
    regions={f"region_{i}": (1 / 1.0) for i in range(1)}
)
polarization_metrics_four_regions, final_df_four_regions = run_axelrod(
    display_name="Four Regions",
    passive_selection=select_passive_by_region,
    regions={f"region_{i}": (1 / 4.0) for i in range(4)}
)
polarization_metrics_twenty_regions, final_df_twenty_regions = run_axelrod(
    display_name="Twenty Regions",
    passive_selection=select_passive_by_region,
    regions={f"region_{i}": (1 / 20.0) for i in range(20)}
)
polarization_metrics_df = polarization_metrics_classic.join(polarization_metrics_single_region)
polarization_metrics_df = polarization_metrics_df.join(polarization_metrics_four_regions)
polarization_metrics_df = polarization_metrics_df.join(polarization_metrics_twenty_regions)
show_polarization_metrics(polarization_metrics_df)
