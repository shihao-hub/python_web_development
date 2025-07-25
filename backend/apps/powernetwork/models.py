from django.db import models


# -------------------------------------------------------------------------------------------------------------------- #
# 贵州山区柔性配电网多维度评估系统 - 数据模型 - 练手版
# -------------------------------------------------------------------------------------------------------------------- #
class Bus(models.Model):
    bus_i = models.FloatField(verbose_name="总线唯一标识符", primary_key=True)
    type = models.FloatField(verbose_name="总线类型")
    Pd = models.FloatField(verbose_name="有功功率需求")
    Qd = models.FloatField(verbose_name="无功功率需求")
    Gs = models.FloatField(verbose_name="并联电导")
    Bs = models.FloatField(verbose_name="并联电纳")
    area = models.FloatField(verbose_name="区域编号")
    Vm = models.FloatField(verbose_name="电压幅值")
    Va = models.FloatField(verbose_name="电压相角")
    baseKV = models.FloatField(verbose_name="基准电压")
    zone = models.FloatField(verbose_name="分区编号")
    Vmax = models.FloatField(verbose_name="电压上限")
    Vmin = models.FloatField(verbose_name="电压下限")


class Generator(models.Model):
    bus = models.FloatField(verbose_name="bus")
    Pg = models.FloatField(verbose_name="Pg")
    Qg = models.FloatField(verbose_name="Qg")
    Qmax = models.FloatField(verbose_name="Qmax")
    Qmin = models.FloatField(verbose_name="Qmin")
    Vg = models.FloatField(verbose_name="Vg")
    mBase = models.FloatField(verbose_name="mBase")
    status = models.FloatField(verbose_name="status")
    Pmax = models.FloatField(verbose_name="Pmax")
    Pmin = models.FloatField(verbose_name="Pmin")
    Pc1 = models.FloatField(verbose_name="Pc1")
    Pc2 = models.FloatField(verbose_name="Pc2")
    Qc1min = models.FloatField(verbose_name="Qc1min")
    Qc1max = models.FloatField(verbose_name="Qc1max")
    Qc2min = models.FloatField(verbose_name="Qc2min")
    Qc2max = models.FloatField(verbose_name="Qc2max")
    ramp_agc = models.FloatField(verbose_name="ramp_agc")
    ramp_10 = models.FloatField(verbose_name="ramp_10")
    ramp_30 = models.FloatField(verbose_name="ramp_30")
    ramp_q = models.FloatField(verbose_name="ramp_q")
    apf = models.FloatField(verbose_name="apf")


class Branch(models.Model):
    fbus = models.FloatField(verbose_name="fbus")
    tbus = models.FloatField(verbose_name="tbus")
    r = models.FloatField(verbose_name="r")
    x = models.FloatField(verbose_name="x")
    b = models.FloatField(verbose_name="b")
    rateA = models.FloatField(verbose_name="rateA")
    rateB = models.FloatField(verbose_name="rateB")
    rateC = models.FloatField(verbose_name="rateC")
    ratio = models.FloatField(verbose_name="ratio")
    angle = models.FloatField(verbose_name="angle")
    status = models.FloatField(verbose_name="status")
    angmin = models.FloatField(verbose_name="angmin")
    angmax = models.FloatField(verbose_name="angmax")


class GeneratorCost(models.Model):
    startup = models.FloatField(verbose_name="startup")
    shutdown = models.FloatField(verbose_name="shutdown")
    n = models.FloatField(verbose_name="n")
    x1 = models.FloatField(verbose_name="x1")
    y1 = models.FloatField(verbose_name="y1")
    xn = models.FloatField(verbose_name="xn")
    yn = models.FloatField(verbose_name="yn")
