from progress import Progress


def test_connection_points_start_from_zero():
    progress = Progress()

    assert progress.connection_points == 0


def test_add_connection_point():
    progress = Progress()

    progress.add_connection_point()

    assert progress.connection_points == 1


def test_phone_answered_flag():
    progress = Progress()

    progress.mark_phone_answered()

    assert progress.phone_answered is True


def test_ticket_found_flag():
    progress = Progress()

    progress.mark_ticket_found()

    assert progress.ticket_found is True


def test_symbol_puzzle_solved_flag():
    progress = Progress()

    progress.mark_symbol_puzzle_solved()

    assert progress.symbol_puzzle_solved is True


def test_ending_shown_flag():
    progress = Progress()

    progress.mark_ending_shown()

    assert progress.ending_shown is True