import logging
import argparse
import sys

from openapi_spec_validator import (
    openapi_v2_spec_validator, openapi_v3_spec_validator,
)
from openapi_spec_validator.exceptions import ValidationError
from openapi_spec_validator.readers import read_from_stdin, read_from_filename

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.WARNING
)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Absolute or relative path to file")
    parser.add_argument(
        '--schema',
        help="OpenAPI schema (default: 3.0.0)",
        type=str,
        choices=['2.0', '3.0.0'],
        default='3.0.0'
    )
    args = parser.parse_args(args)

    # choose source
    reader = read_from_filename
    if args.filename in ['-', '/-']:
        reader = read_from_stdin

    # read source
    try:
        spec, spec_url = reader(args.filename)
    except Exception as exc:
        print(exc)
        sys.exit(1)

    # choose the validator
    validators = {
        '2.0': openapi_v2_spec_validator,
        '3.0.0': openapi_v3_spec_validator,
    }
    validator = validators[args.schema]

    # validate
    try:
        validator.validate(spec, spec_url=spec_url)
    except ValidationError as exc:
        print(exc)
        sys.exit(1)
    except Exception as exc:
        print(exc)
        sys.exit(2)
    else:
        print('OK')


if __name__ == '__main__':
    main()
