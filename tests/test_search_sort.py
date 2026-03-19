import pytest


@pytest.mark.parametrize(
    "game_name, n",
    [
        ("The Witcher", 10),
        ("Fallout", 20),
    ]
)
def test_search_results_sorted_by_price_desc(main_page, game_name, n):
    search_page = main_page.search(game_name)
    search_page.set_sort_by_price_desc()
    current_sort = search_page.get_current_sort_value()
    assert current_sort == "Price_DESC", (
        f"Expected current sort to be 'Price_DESC', but got {current_sort!r}"
    )

    prices = search_page.get_first_n_prices(n)

    assert prices == sorted(prices, reverse=True), (
        f"Expected paid prices sorted in descending order for game {game_name!r}, "
        f"but got: {prices}"
    )