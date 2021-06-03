# Copyright © Simphony Project Contributors
# Licensed under the terms of the MIT License
# (see simphony/__init__.py for details)

import filecmp
import os

import numpy as np
import pytest

from simphony.formatters import *
from simphony.layout import Circuit
from simphony.libraries import siepic
from simphony.models import Model
from simphony.simulators import SweepSimulator
from simphony.tools import wl2freq

waveguide_150_json = '{"freqs": [187370286250000.0, 187625211809523.8, 187880137369047.62, 188135062928571.44, 188389988488095.25, 188644914047619.03, 188899839607142.84, 189154765166666.66, 189409690726190.47, 189664616285714.28, 189919541845238.1, 190174467404761.9, 190429392964285.72, 190684318523809.53, 190939244083333.34, 191194169642857.12, 191449095202380.94, 191704020761904.75, 191958946321428.56, 192213871880952.38, 192468797440476.2, 192723723000000.0, 192978648559523.8, 193233574119047.62, 193488499678571.44, 193743425238095.22, 193998350797619.03, 194253276357142.84, 194508201916666.66, 194763127476190.47, 195018053035714.28, 195272978595238.1, 195527904154761.9, 195782829714285.72, 196037755273809.53, 196292680833333.3, 196547606392857.12, 196802531952380.94, 197057457511904.75, 197312383071428.56, 197567308630952.38, 197822234190476.2, 198077159750000.0, 198332085309523.8, 198587010869047.62, 198841936428571.4, 199096861988095.22, 199351787547619.03, 199606713107142.84, 199861638666666.66], "name": "Waveguide component", "pins": ["pin1", "pin2"], "s_params": [[[{"r": 0.0, "i": 0.0}, {"r": 0.9819372843478702, "i": -0.10914188947302844}], [{"r": 0.9819372843478702, "i": -0.10914188947302844}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.9819660561675987, "i": -0.10888272114924973}], [{"r": -0.9819660561675987, "i": -0.10888272114924973}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9342309642469012, "i": 0.32144251099149607}], [{"r": 0.9342309642469012, "i": 0.32144251099149607}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.8411620645449615, "i": -0.5182269421794576}], [{"r": -0.8411620645449615, "i": -0.5182269421794576}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.7073784390613481, "i": 0.6897307636906906}], [{"r": 0.7073784390613481, "i": 0.6897307636906906}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.5394525325558538, "i": -0.8277099416760005}], [{"r": -0.5394525325558538, "i": -0.8277099416760005}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.34558166856357203, "i": 0.9255733859522054}], [{"r": 0.34558166856357203, "i": 0.9255733859522054}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.13518340962229414, "i": -0.978692100812663}], [{"r": -0.13518340962229414, "i": -0.978692100812663}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.08156506779099679, "i": 0.9846115590152611}], [{"r": -0.08156506779099679, "i": 0.9846115590152611}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.2942209206900538, "i": -0.9431579042018944}], [{"r": 0.2942209206900538, "i": -0.9431579042018944}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.4925788738903655, "i": 0.8564337892838606}], [{"r": -0.4925788738903655, "i": 0.8564337892838606}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.6671595040380727, "i": -0.7287050010819781}], [{"r": 0.6671595040380727, "i": -0.7287050010819781}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.8096592996367279, "i": 0.566184246462206}], [{"r": -0.8096592996367279, "i": 0.566184246462206}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9133412902275477, "i": -0.37672333348983195}], [{"r": 0.9133412902275477, "i": -0.37672333348983195}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.9733480946266168, "i": 0.16942924516430902}], [{"r": -0.9733480946266168, "i": 0.16942924516430902}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9869231255652772, "i": 0.04577692273053116}], [{"r": 0.9869231255652772, "i": 0.04577692273053116}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.9535302097155838, "i": -0.25863665940845976}], [{"r": -0.9535302097155838, "i": -0.25863665940845976}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.874866814128509, "i": 0.4590433966052074}], [{"r": 0.874866814128509, "i": 0.4590433966052074}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.7547711725938214, "i": -0.6375211835316223}], [{"r": -0.7547711725938214, "i": -0.6375211835316223}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.5990286338311728, "i": 0.7856700823377275}], [{"r": 0.5990286338311728, "i": 0.7856700823377275}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.415087270397498, "i": -0.896557494187722}], [{"r": -0.415087270397498, "i": -0.896557494187722}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.21169697367451903, "i": 0.9650373950097804}], [{"r": 0.21169697367451903, "i": 0.9650373950097804}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.0015102744047119844, "i": -0.9879830471730956}], [{"r": 0.0015102744047119844, "i": -0.9879830471730956}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.21447867198425702, "i": 0.9644229786219749}], [{"r": -0.21447867198425702, "i": 0.9644229786219749}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.4172035243948595, "i": -0.8955746767649925}], [{"r": 0.4172035243948595, "i": -0.8955746767649925}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.600200384463583, "i": 0.784775306008019}], [{"r": -0.600200384463583, "i": 0.784775306008019}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.7549464650449498, "i": -0.6373135941954692}], [{"r": 0.7549464650449498, "i": -0.6373135941954692}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.8742739069529043, "i": 0.4601716180421356}], [{"r": -0.8742739069529043, "i": 0.4601716180421356}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9526969465318981, "i": -0.2616893396739929}], [{"r": 0.9526969465318981, "i": -0.2616893396739929}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.986658297367269, "i": 0.05116821930197158}], [{"r": -0.986658297367269, "i": 0.05116821930197158}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9746839767175536, "i": 0.16156710048852221}], [{"r": 0.9746839767175536, "i": 0.16156710048852221}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.9174401780132309, "i": -0.3666282888666179}], [{"r": -0.9174401780132309, "i": -0.3666282888666179}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.8176904068508444, "i": 0.5545224801343165}], [{"r": 0.8176904068508444, "i": 0.5545224801343165}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.6801557416700721, "i": -0.7165898056094903}], [{"r": -0.6801557416700721, "i": -0.7165898056094903}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.5112855361098615, "i": 0.845399244732963}], [{"r": 0.5112855361098615, "i": 0.845399244732963}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.318949944220238, "i": -0.9350848707535161}], [{"r": -0.318949944220238, "i": -0.9350848707535161}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.11206913976317646, "i": 0.9816075032022495}], [{"r": 0.11206913976317646, "i": 0.9816075032022495}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.09980313646224996, "i": -0.9829303720928102}], [{"r": 0.09980313646224996, "i": -0.9829303720928102}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.3069221494213715, "i": 0.9391014730181069}], [{"r": -0.3069221494213715, "i": 0.9391014730181069}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.49980031442270156, "i": -0.8522396541661162}], [{"r": 0.49980031442270156, "i": -0.8522396541661162}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.6696403234786891, "i": 0.7264259216200709}], [{"r": -0.6696403234786891, "i": 0.7264259216200709}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.8087335654017669, "i": -0.5675057732065453}], [{"r": 0.8087335654017669, "i": -0.5675057732065453}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.9108059431748774, "i": 0.3828123774220667}], [{"r": -0.9108059431748774, "i": 0.3828123774220667}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9712957793597037, "i": -0.18082392382712695}], [{"r": 0.9712957793597037, "i": -0.18082392382712695}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.9875517542725215, "i": -0.029228668520445485}], [{"r": -0.9875517542725215, "i": -0.029228668520445485}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.9589425851857615, "i": 0.23778540902978335}], [{"r": 0.9589425851857615, "i": 0.23778540902978335}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.8868742497382736, "i": -0.4353927509518127}], [{"r": -0.8868742497382736, "i": -0.4353927509518127}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.7747147927033525, "i": 0.6131311216997669}], [{"r": 0.7747147927033525, "i": 0.6131311216997669}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": -0.6276309383382572, "i": -0.7630151949147878}], [{"r": -0.6276309383382572, "i": -0.7630151949147878}, {"r": 0.0, "i": 0.0}]], [[{"r": 0.0, "i": 0.0}, {"r": 0.4523446721680537, "i": 0.8783490650028545}], [{"r": 0.4523446721680537, "i": 0.8783490650028545}, {"r": 0.0, "i": 0.0}]]], "subcircuit": null}'


@pytest.fixture(scope="module")
def freqs():
    return np.linspace(wl2freq(1600e-9), wl2freq(1500e-9))


@pytest.fixture(scope="class")
def mzi():
    gc_input = siepic.GratingCoupler()
    y_splitter = siepic.YBranch()
    wg_long = siepic.Waveguide(length=150e-6)
    wg_short = siepic.Waveguide(length=50e-6)
    y_recombiner = siepic.YBranch()
    gc_output = siepic.GratingCoupler()

    y_splitter.multiconnect(gc_input, wg_long, wg_short)
    y_recombiner.multiconnect(gc_output, wg_short, wg_long)

    return y_splitter.circuit


@pytest.fixture(scope="class")
def mzi4(freqs):
    y1 = siepic.YBranch()
    gc1 = siepic.GratingCoupler()
    wg1 = siepic.Waveguide(length=67.730e-6)
    wg2 = siepic.Waveguide(length=297.394e-6)
    y2 = siepic.YBranch()
    gc2 = siepic.GratingCoupler()
    wg3 = siepic.Waveguide(length=256.152e-6)
    simulator = SweepSimulator(freqs[0], freqs[-1], len(freqs))

    y1.rename_pins("N$0", "N$2", "N$1")
    gc1.rename_pins("ebeam_gc_te1550_detector2", "N$0")
    wg1.rename_pins("N$1", "N$4")
    wg2.rename_pins("N$2", "N$5")
    y2.rename_pins("N$6", "N$5", "N$4")
    gc2.rename_pins("ebeam_gc_te1550_laser1", "N$3")
    wg3.rename_pins("N$6", "N$3")

    y1.multiconnect(gc1["N$0"], wg2, wg1)
    y2.multiconnect(wg3, wg2, wg1)
    wg3.connect(gc2["N$3"])

    simulator.multiconnect(gc2, gc1)

    return simulator.circuit


@pytest.fixture(scope="class")
def waveguide():
    return siepic.Waveguide(length=150e-6)


class TestModelJSONFormatter:
    def test_format(self, freqs, waveguide):
        assert waveguide_150_json == waveguide.to_string(
            freqs, formatter=ModelJSONFormatter()
        )

    def test_parse(self, freqs, waveguide):
        waveguide2 = Model.from_string(waveguide_150_json)
        assert (
            np.around(waveguide.s_parameters(freqs), decimals=13)
            == np.around(waveguide2.s_parameters(freqs), decimals=13)
        ).all()


class TestCircuitJSONFormatter:
    def test_format(self, freqs, mzi):
        json = os.path.join(os.path.dirname(__file__), "mzi.json")
        temp = os.path.join(os.path.dirname(__file__), "mzi.temp.json")

        mzi.to_file(temp, freqs, formatter=CircuitJSONFormatter())

        assert filecmp.cmp(json, temp)
        os.unlink(temp)

    def test_parse(self, freqs, mzi):
        json = os.path.join(os.path.dirname(__file__), "mzi.json")
        mzi2 = Circuit.from_file(json, formatter=CircuitJSONFormatter())

        assert (
            np.around(mzi.s_parameters(freqs), decimals=13)
            == np.around(mzi2.s_parameters(freqs), decimals=13)
        ).all()


class TestCircuitSiEPICFormatter:
    def test_parse(self, freqs, mzi4):
        spi = os.path.join(
            os.path.dirname(__file__),
            "..",
            "plugins",
            "siepic",
            "tests",
            "spice",
            "MZI4",
            "MZI4_main.spi",
        )

        mzi42 = Circuit.from_file(spi, formatter=CircuitSiEPICFormatter())

        assert (
            np.around(mzi4.s_parameters(freqs), decimals=13)
            == np.around(mzi42.s_parameters(freqs), decimals=13)
        ).all()
