import pytest


@pytest.mark.parametrize(
    "game_name, n",
    [
        ("The Witcher", 10),
        ("Fallout", 20),
    ]
)
def test_search_results_sorted_by_price_desc(main_page, game_name, n):
    search_page = main_page.open_advanced_search()

    search_page.search_for_game(game_name)
    search_page.set_sort_by_price_desc()

    prices = search_page.get_first_n_prices(n)

    assert len(prices) == n, (
        f"Expected {n} prices for game {game_name!r}, but got {len(prices)}. "
        f"Actual prices: {prices}"
    )

    assert search_page.are_prices_sorted_desc(prices), (
        f"Expected prices sorted in descending order for game {game_name!r}, "
        f"but got: {prices}"
    )