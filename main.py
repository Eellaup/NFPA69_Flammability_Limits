from src.NFPA_FL import NFPA_FL


def main():
    # Example in NFPA 69 (2019)
    flam = {
        'C4H8O2' : 0.636/10,
        'C2H5OH' : 0.208/10,
        'C7H8' : 0.157/10
    }
    dil = {}

    fl = NFPA_FL(flam,dil)

    print('LFL: ',fl.LFL())
    print('UFL: ',fl.UFL())

if __name__ == '__main__':
    main()