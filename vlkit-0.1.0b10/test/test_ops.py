import sys, os
import torch
import torch.nn as nn
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, root_dir)
import vlkit
from vlkit.ops import ConvModule, InvertedResidual, SqueezeExcite, DualBN

print(vlkit.__file__)


def test_inverted_residual():
    print("================ InvertedResidual ================")
    x = torch.zeros(3, 64, 32, 32)

    model = InvertedResidual(64, 64, expand_ratio=4, stride=1, se_ratio=None, act_layer=nn.ReLU)
    model(x)
    print(model)

    model = InvertedResidual(64, 64, expand_ratio=4, stride=1, se_ratio=None, act_layer=nn.PReLU)
    model(x)
    print(model)

    model = InvertedResidual(64, 64, expand_ratio=4, stride=1, se_ratio=1/4, act_layer=nn.PReLU)
    model(x)
    print(model)


def test_conv_module():
    print("================ Test ConvModule ================")
    x = torch.zeros(2, 64, 32, 32)

    model = ConvModule(64, 64, kernel_size=3, stride=1, bias=False)
    print(model)
    model(x)

    model = ConvModule(64, 64, kernel_size=3, stride=2, bias=False, act_layer=nn.PReLU, act_args={"num_parameters": -1})
    print(model)
    model(x)

    model = ConvModule(64, 64, kernel_size=3, stride=2, bias=False, act_layer=nn.PReLU, act_args={"num_parameters": 1})
    print(model)
    model(x)


def test_squeeze_excite():
    print("================ Test SqueezeExcite ================")
    x = torch.zeros(2, 64, 32, 32)

    model = SqueezeExcite(64)
    model(x)
    print(model)

    model = SqueezeExcite(64, act_layer=nn.PReLU)
    model(x)
    print(model)

    model = SqueezeExcite(64, act_layer=nn.PReLU, act_args={"num_parameters": 16})
    model(x)
    print(model)


def test_dual_bn():
    num_bns = 5
    bs = 32
    dual_bn = DualBN(in_chs=64, num_bns=num_bns)

    x = torch.rand(bs, 64, 32, 32)

    # 多 BN 融合
    weights = torch.nn.functional.softmax(torch.rand(bs, num_bns), dim=1)
    y = dual_bn(x, weights)

    # 单 BN 选择
    weights = torch.ones(bs,).long()
    y = dual_bn(x, weights)


def main():
    test_inverted_residual()
    test_conv_module()
    test_squeeze_excite()
    test_dual_bn()


if __name__ == "__main__":
    main()

