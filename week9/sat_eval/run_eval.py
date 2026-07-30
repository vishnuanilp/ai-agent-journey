from testset import TESTS
from bot import ask
from judge import judge

def run(k):
    total = {"accuracy": 0, "relevance": 0, "format": 0}
    for t in TESTS:
        answer = ask(t["q"], k=k)
        score = judge(t["q"], t["a"], answer)
        for key in total:
            total[key] += score[key]
        print(f'k={k} {score["accuracy"]}/{score["relevance"]}/{score["format"]}  {t["q"]}')
    overall = sum(total.values())
    print(f'\nk={k}  accuracy {total["accuracy"]}  relevance {total["relevance"]}'
          f'  format {total["format"]}  TOTAL {overall}/300\n')
    return total

if __name__ == "__main__":
    run(k=4)