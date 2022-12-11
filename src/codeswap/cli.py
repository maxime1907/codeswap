import asyncio
import logging
import os
from typing import Dict, Optional

import click
import yaml
from revChatGPT.revChatGPT import AsyncChatbot as Chatbot

logger = logging.getLogger(__name__)


def convert_content(
    *,
    dry_run: bool,
    config: Dict[str, str],
    source: str,
    destination: str,
    contents: str,
) -> str:
    output: str = ""

    if dry_run:
        return output

    chatbot = Chatbot(config["chatgpt"], conversation_id=None)
    keyphrase = f"Convert the following code written in {source} to {destination} without any explanation and return only converted code in a code block:\n"
    query = f"{keyphrase}{contents}"
    responses = []

    response = asyncio.run(chatbot.get_chat_response(query, output="text"))
    responses.append(response)

    for resp in responses:
        raw_message: str = resp["message"]
        message = raw_message
        if raw_message.startswith("```"):
            message = message[3:]
        if message.endswith("```"):
            message = message[:-3]
        output += message

    return output


def save_content(
    *,
    dry_run: bool,
    input_file_path: str,
    output_contents: str,
    output: str,
    output_extension: str,
) -> None:
    file_name = os.path.basename(input_file_path)
    file_name_without_extension, file_ext = os.path.splitext(file_name)

    abs_output_path = os.path.abspath(output)

    file_path_output = (
        f"{abs_output_path}/{file_name_without_extension}{output_extension}"
    )
    logger.info(f"Writing the output to {file_path_output}")
    if dry_run:
        return

    if not os.path.exists(abs_output_path):
        os.makedirs(abs_output_path)

    with open(file_path_output, "w+") as file:
        file.write(output_contents)


def process_file(
    dry_run: bool,
    config: Dict[str, str],
    source: str,
    destination: str,
    input: str,
    input_extension: str,
    output: str,
    output_extension: str,
    file_path: str,
) -> None:
    file_name = os.path.basename(file_path)
    _file_name_without_extension, file_ext = os.path.splitext(file_name)
    if file_ext != input_extension:
        return

    # Do something with the file (e.g. read its contents)
    with open(file_path, 'r') as f:
        input_contents = f.read()
        logger.info(f"Converting {file_path}...")
        output_contents = convert_content(
            dry_run=dry_run,
            config=config,
            source=source,
            destination=destination,
            contents=input_contents,
        )
        save_content(
            dry_run=dry_run,
            input_file_path=file_path,
            output_contents=output_contents,
            output=output,
            output_extension=output_extension,
        )


def codeswap(
    *,
    dry_run: bool,
    config: Dict[str, str],
    source: str,
    destination: str,
    input: str,
    input_extension: str,
    output: str,
    output_extension: str,
) -> None:
    logger.info(f"Converting {source} in {input} to {destination} in {output}")

    if os.path.isdir(input):
        for root, _dirs, files in os.walk(input):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(
                    dry_run=dry_run,
                    config=config,
                    source=source,
                    destination=destination,
                    input=input,
                    input_extension=input_extension,
                    output=output,
                    output_extension=output_extension,
                    file_path=file_path,
                )
    elif os.path.isfile(input):
        file_path = os.path.abspath(input)
        process_file(
            dry_run=dry_run,
            config=config,
            source=source,
            destination=destination,
            input=input,
            input_extension=input_extension,
            output=output,
            output_extension=output_extension,
            file_path=file_path,
        )
    else:
        logger.error(f'{input} is not a valid filepath')
        exit(84)


@click.command()
@click.option('--dry-run', is_flag=True, help="Simulated execution")
@click.option('-v', '--verbose', count=True, help="Verbosity level")
@click.option(
    '-c', '--config', required=True, default="config.yml", help="Configuration filepath"
)
@click.option('-s', '--source', required=True, help="Source language")
@click.option('-d', '--destination', required=True, help="Destination language")
@click.option(
    '-i', '--input', required=True, help="Directory containing the source code"
)
@click.option('-ie', '--input-extension', help="Input extension")
@click.option(
    '-o',
    '--output',
    required=True,
    help="Output directory containing the destination code",
)
@click.option('-oe', '--output-extension', help="Output extension")
def cli(
    config: str,
    source: str,
    destination: str,
    input: str,
    input_extension: Optional[str],
    output: str,
    output_extension: Optional[str],
    verbose: int,
    dry_run: bool,
) -> None:

    log_level = logging.ERROR
    if verbose > 2:
        log_level = logging.DEBUG
    elif verbose > 1:
        log_level = logging.INFO
    elif verbose > 0:
        log_level = logging.WARNING

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S%z',
    )

    with open(config, "r") as file:
        configdata = yaml.load(file, Loader=yaml.FullLoader)

    if not input_extension:
        input_extension = input

    if not output_extension:
        output_extension = output

    if input_extension[0] != ".":
        input_extension = f".{input_extension}"

    if output_extension[0] != ".":
        output_extension = f".{output_extension}"

    codeswap(
        dry_run=dry_run,
        config=configdata,
        source=source,
        destination=destination,
        input=input,
        input_extension=input_extension,
        output=output,
        output_extension=output_extension,
    )
