#!/usr/bin/env python3
# モジュールのインポート
import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from strip_ansi import strip_ansi
from functools import reduce


def main():
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()

    fTyp = [("", "*")]

    iDir = os.path.abspath(os.path.dirname(__file__))
    filename = tkinter.filedialog.askopenfilename(
        filetypes=fTyp, initialdir=iDir)

    target = []
    plain = []
    with open(filename, "r", encoding="utf8") as fobj:
        for i, l in enumerate(fobj, 1):
            str = strip_ansi(l)
            if '"patientList"' not in str and '"queryList"' not in str:
                plain.append(str)
            if 'ERROR' in str and not 'The Network Adapter could not establish the connection' in str:
                target.append(i)
    target = reduce(lambda acc, n: acc + [n] if not any(e < n + 1000 and e > n - 1000 for e in acc) else acc,
                    target,
                    [])
    dirname = filename.split('/').pop()
    os.makedirs(dirname, exist_ok=True)
    for i, t in enumerate(target):
        with open(f'/out/{dirname}/result{i:02}.log', "w", encoding="utf8") as wf:
            start = t - 1000 if t - 1000 > 0 else 0
            end = t + 1000 if t + 1000 <= len(plain) else len(plain)
            for s in plain[start:end]:
                wf.write(s)


if __name__ == "__main__":
    main()
