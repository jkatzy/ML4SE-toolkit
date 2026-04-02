from ml4setk import CommentQuery, FIMInput


def main():
    sample = "prefix\n// explain this branch\nsuffix"
    match = CommentQuery("java").parse(sample)[0]
    model_input, ground_truth = FIMInput(
        "<fim_prefix>",
        "<fim_suffix>",
        "<fim_middle>",
    ).generate(match)

    print(model_input)
    print(ground_truth)


if __name__ == "__main__":
    main()
