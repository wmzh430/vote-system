
// vote-delegate.spec

// certoraRun src/VoteDelegate.sol src/DSChief.sol src/Gov.sol src/Iou.sol --link VoteDelegate:chief=DSChief VoteDelegate:gov=Gov VoteDelegate:iou=Iou DSChief:GOV=Gov DSChief:IOU=Iou --verify VoteDelegate:src/specs/vote-delegate.spec --loop_iter 4

// certoraRun src/VoteDelegate.sol src/DSChief.sol --link VoteDelegate:chief=DSChief --verify VoteDelegate:src/specs/vote-delegate.spec --loop_iter 2

// certoraRun src/VoteDelegate.sol src/DSChief.sol src/Gov.sol --link VoteDelegate:chief=DSChief VoteDelegate:gov=Gov DSChief:GOV=Gov --verify VoteDelegate:src/specs/vote-delegate.spec --loop_iter 3

using DSChief as chiefInstance
using Gov as govInstance
using Iou as iouInstance

rule lock(uint256 wad) {
    env e;

    require(e.msg.sender != currentContract);
    require(e.msg.sender != chiefInstance);
    require(e.msg.sender != govInstance);
    require(e.msg.sender != iouInstance);

    uint256 senderStakeBefore = stake(e, e.msg.sender);
    uint256 chiefDepositsBefore = chiefInstance.deposits(e, currentContract);
    uint256 senderGovBalanceBefore = govInstance.balanceOf(e, e.msg.sender);
    uint256 senderIouBalanceBefore = iouInstance.balanceOf(e, e.msg.sender);
    uint256 chiefGovBalanceBefore = govInstance.balanceOf(e, chiefInstance);

    lock(e, wad);

    uint256 senderStakeAfter = stake(e, e.msg.sender);
    uint256 chiefDepositsAfter = chiefInstance.deposits(e, currentContract);
    uint256 senderGovBalanceAfter = govInstance.balanceOf(e, e.msg.sender);
    uint256 senderIouBalanceAfter = iouInstance.balanceOf(e, e.msg.sender);
    uint256 chiefGovBalanceAfter = govInstance.balanceOf(e, chiefInstance);

    assert(senderStakeAfter == senderStakeBefore + wad, "chief deposit error");
    assert(chiefDepositsAfter == chiefDepositsBefore + wad, "chief deposit error");
    assert(senderGovBalanceAfter == senderGovBalanceBefore - wad, "sender gov balance error");
    assert(senderIouBalanceAfter == senderIouBalanceBefore + wad, "iou balance error");
    assert(chiefGovBalanceAfter == chiefGovBalanceBefore + wad, "chief gov balance error");
}
