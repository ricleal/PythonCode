from enum import Enum


class Provider(str, Enum):
    aws = "AWS"
    microsoft = "MICROSOFT"
    google = "GOOGLE"
    okta = "OKTA"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None


if __name__ == "__main__":
    print(Provider("aws"))  # Provider.aws
    print(Provider("AWS"))  # Provider.aws

    if "aws" in Provider:
        print("aws is in Provider")
    if "AWS" in Provider:
        print("AWS is in Provider")
