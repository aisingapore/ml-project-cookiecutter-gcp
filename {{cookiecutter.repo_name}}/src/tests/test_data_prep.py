import pytest
import tensorflow as tf
from {{cookiecutter.src_package_name}} import data_prep

@pytest.fixture
def text_with_tags_punct():
    text = "This text has tags!<br /><br />Can we remove them? Let's see."
    return text

@pytest.fixture
def correct_tensor():
    correct_result = "this text has tags can we remove them let see "
    correct_result_tensor = tf.convert_to_tensor(correct_result)
    return correct_result_tensor


def test_tag_punct_remover(text_with_tags_punct, correct_tensor):
    result = data_prep.process_text.tag_punct_remover(text_with_tags_punct)
    assert result == correct_tensor


def test_process_file(text_with_tags_punct, correct_tensor, tmp_path):
    txt_file_path = tmp_path / "test.txt"
    txt_file_path.write_text(text_with_tags_punct)
    result = data_prep.process_text.process_file(str(txt_file_path))
    assert result == correct_tensor
