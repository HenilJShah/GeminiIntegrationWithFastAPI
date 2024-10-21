from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, field_validator, Field


class Question(BaseModel):
    """
    Represents a question in a section of the sample paper.

    Attributes:
        question (str): The text of the question.
        answer (str): The answer to the question.
        type (str): The type of question, which can be 'short', 'long', or 'multiple_choice'.
        question_slug (str): A slug identifier for the question.
        reference_id (str): An ID used to reference the question.
        hint (Optional[str]): An optional hint for the question.
        params (Optional[dict]): Additional parameters for the question.
    """

    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: str
    hint: Optional[str] = None
    params: Optional[dict] = {}

    @field_validator("type")
    def validate_question_type(cls, value):
        """
        Validates the type of the question.

        Args:
            value (str): The type of the question.

        Raises:
            ValueError: If the question type is not one of 'short', 'long', or 'multiple_choice'.

        Returns:
            str: The validated question type.
        """
        allowed_types = {"short", "long", "multiple_choice"}
        if value not in allowed_types:
            raise ValueError(f"Question type must be one of {allowed_types}")
        return value


class Section(BaseModel):
    """
    Represents a section in the sample paper.

    Attributes:
        marks_per_question (int): The number of marks allocated per question.
        type (str): The type of section, which can be 'default' or 'custom'.
        questions (List[Question]): A list of questions in the section.
    """

    marks_per_question: int
    type: str
    questions: List[Question]

    @field_validator("type")
    def validate_section_type(cls, value):
        """
        Validates the type of the section.

        Args:
            value (str): The type of the section.

        Raises:
            ValueError: If the section type is not 'default' or 'custom'.

        Returns:
            str: The validated section type.
        """
        allowed_types = {"default", "custom"}
        if value not in allowed_types:
            raise ValueError(f"Section type must be one of {allowed_types}")
        return value


class PaperParams(BaseModel):
    """
    Represents parameters associated with a sample paper.

    Attributes:
        board (str): The educational board (e.g., CBSE, ICSE).
        grade (int): The grade level of the paper.
        subject (str): The subject of the paper.
    """

    board: str
    grade: int
    subject: str


class SamplePaper(BaseModel):
    """
    Represents a sample paper with multiple sections.

    Attributes:
        p_id (Optional[str]): The unique identifier for the paper.
        title (str): The title of the paper.
        type (str): The type of the paper, which can be 'previous_year', 'mock', or 'sample'.
        time (int): The total time allocated for the paper, in minutes.
        marks (int): The total marks for the paper.
        params (PaperParams): Additional parameters for the paper.
        tags (List[str]): A list of tags associated with the paper.
        chapters (List[str]): A list of chapters covered in the paper.
        sections (List[Section]): A list of sections within the paper.
    """

    p_id: Optional[str] = None
    title: str
    type: str
    time: int
    marks: int
    params: PaperParams
    tags: List[str]
    chapters: List[str]
    sections: List[Section]

    @field_validator("type")
    def validate_paper_type(cls, value):
        """
        Validates the type of the paper.

        Args:
            value (str): The type of the paper.

        Raises:
            ValueError: If the paper type is not one of 'previous_year', 'mock', or 'sample'.

        Returns:
            str: The validated paper type.
        """
        allowed_types = {"previous_year", "mock", "sample"}
        if value not in allowed_types:
            raise ValueError(f"Paper type must be one of {allowed_types}")
        return value


class StandardResponse(BaseModel):
    """
    Represents a standard API response structure.

    Attributes:
        code (int): The response code (e.g., 200 for success, 404 for not found).
        status (str): The status of the response (e.g., 'success', 'error').
        message (str): A descriptive message providing details about the response.
        data (Optional[Any]): The data payload included in the response.
    """

    code: int
    status: str
    message: str
    data: Optional[Any] = None


class Tasks(BaseModel):
    """
    Represents a task related to the processing of a file.

    Attributes:
        t_id (Optional[str]): The unique identifier for the task.
        task_status (str): The current status of the task.
        extract_data (Optional[str]): Extracted data related to the task, if any.
        file_path (Optional[str]): The path of the file being processed.
        file_type (Optional[str]): The type of the file (e.g., 'pdf', 'text').
        datetime (float): The timestamp of the task creation, in Unix format.
    """

    t_id: Optional[str] = None
    task_status: str
    extract_data: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    datetime: float = Field(default_factory=lambda: datetime.now().now())
