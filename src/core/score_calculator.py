from core.semantic_score import SemanticScore
from util.file_util import FileUtil

semantic_dir = "../../resources/semantic"


def load_semantic():
    semantic = None
    semantic_file_path = FileUtil.get_file_paths_from_directory(semantic_dir)
    for semantic_file_path in semantic_file_path:
        with open(semantic_file_path) as semantic_data:
            semantic = SemanticScore(semantic_data)
    return semantic


class ScoreCalculatorService:
    def __init__(self):
        self.semantic = load_semantic()

    def process_statistics(self, topic, sentences_by_topic, hotel_info):
        pass
