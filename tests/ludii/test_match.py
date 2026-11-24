from pathlib import Path

from pyttern.language_processors import LudiiProcessor

GAMES = Path(__file__).parent / "tests_files" / "parse"

PATTERN = """
(end
    (if ?
        (result Mover Win)
    )
)
"""


def text(node):
    return node.start.getInputStream().getText(node.start.start, node.stop.stop)


def find(pattern, game):
    processor = LudiiProcessor()
    pda = processor.create_pda(processor.generate_tree_from_code(pattern))
    code_tree = processor.generate_tree_from_file(GAMES / game)
    return [(text(node), {k: text(v) for k, v in bindings.items()})
            for node, bindings in processor.find_matches(pda, code_tree)]


def test_tic_tac_toe():
    assert find(PATTERN, "Tic-Tac-Toe.lud") == [
        ("(end (if (is Line 3) (result Mover Win)))", {"?1": "(is Line 3)"})
    ]
