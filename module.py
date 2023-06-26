import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone


def main(
    basename, modeldir="MERROW", suffix="musicxml", styleshift="0", numthreads="4"
):
    # commands
    command1 = rf"bin\musicXMLtoLabel.exe score\musicxml\{basename}.{suffix} score\label\full\{basename}.lab score\label\mono\{basename}.lab"
    command2 = rf"bin\NEUTRINO.exe score\label\full\{basename}.lab score\label\timing\{basename}.lab output\{basename}.f0 output\{basename}.mgc output\{basename}.bap model\{modeldir}\ -n {numthreads} -k {styleshift} -m -t"
    command3 = rf"bin\NSF.exe output\{basename}.f0 output\{basename}.mgc output\{basename}.bap .\model\{modeldir}\model_nsf.bin output\{basename}_nsf.wav -l score\label\timing\{basename}.lab -n {numthreads} -m -t"

    # exec
    subprocess.run(command1)
    subprocess.run(command2)
    subprocess.run(command3)

    # rm, rn
    os.remove(f"./output/{basename}.bap")
    os.remove(f"./output/{basename}.f0")
    os.remove(f"./output/{basename}.mgc")
    JST = timezone(timedelta(hours=+9), "JST")
    now = datetime.now(JST).strftime("%Y%m%d%H%M")
    shutil.move(f"./output/{basename}_nsf.wav", f"./output/{now}_{basename}.wav")
