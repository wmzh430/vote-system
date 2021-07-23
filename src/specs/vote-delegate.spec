
// vote-delegate.spec

// certoraRun src/VoteDelegate.sol src/DSChief.sol src/Gov.sol src/Iou.sol --link VoteDelegate:chief=DSChief VoteDelegate:gov=Gov VoteDelegate:iou=Iou DSChief:GOV=Gov DSChief:IOU=Iou --verify VoteDelegate:src/specs/vote-delegate.spec --optimistic_loop

using DSChief as chiefInstance
using Gov as govInstance
using Iou as iouInstance

methods {
    chief() returns (address) envfree
    gov() returns (address) envfree
    iou() returns (address) envfree
    stake(address) returns (uint256) envfree
    chiefInstance.approvals(address) returns (uint256) envfree
    chiefInstance.deposits(address) returns (uint256) envfree
    chiefInstance.GOV() returns (address) envfree
    chiefInstance.IOU() returns (address) envfree
    chiefInstance.MAX_YAYS() returns (uint256) envfree
    chiefInstance.slates(bytes32,uint256) returns (address) envfree
    chiefInstance.votes(address) returns (bytes32) envfree
    govInstance.balanceOf(address) returns (uint256) envfree
    iouInstance.balanceOf(address) returns (uint256) envfree
}

rule lock(uint256 wad) {
    env e;

    require(currentContract.chief() == chiefInstance);
    require(currentContract.gov() == govInstance);
    require(currentContract.iou() == iouInstance);
    require(chiefInstance.GOV() == govInstance);
    require(chiefInstance.IOU() == iouInstance);

    require(e.msg.sender != chiefInstance);

    uint256 senderStakeBefore = stake(e.msg.sender);
    uint256 chiefDepositsBefore = chiefInstance.deposits(currentContract);
    uint256 senderGovBalanceBefore = govInstance.balanceOf(e.msg.sender);
    uint256 senderIouBalanceBefore = iouInstance.balanceOf(e.msg.sender);
    uint256 chiefGovBalanceBefore = govInstance.balanceOf(chiefInstance);

    lock(e, wad);

    uint256 senderStakeAfter = stake(e.msg.sender);
    uint256 chiefDepositsAfter = chiefInstance.deposits(currentContract);
    uint256 senderGovBalanceAfter = govInstance.balanceOf(e.msg.sender);
    uint256 senderIouBalanceAfter = iouInstance.balanceOf(e.msg.sender);
    uint256 chiefGovBalanceAfter = govInstance.balanceOf(chiefInstance);

    assert(senderStakeAfter == senderStakeBefore + wad, "chief deposit error");
    assert(chiefDepositsAfter == chiefDepositsBefore + wad, "chief deposit error");
    assert(senderGovBalanceAfter == senderGovBalanceBefore - wad, "sender gov balance error");
    assert(senderIouBalanceAfter == senderIouBalanceBefore + wad, "iou balance error");
    assert(chiefGovBalanceAfter == chiefGovBalanceBefore + wad, "chief gov balance error");
}

rule free(uint256 wad) {
    env e;

    require(currentContract.chief() == chiefInstance);
    require(currentContract.gov() == govInstance);
    require(currentContract.iou() == iouInstance);
    require(chiefInstance.GOV() == govInstance);
    require(chiefInstance.IOU() == iouInstance);

    require(e.msg.sender != chiefInstance);

    uint256 senderStakeBefore = stake(e.msg.sender);
    uint256 chiefDepositsBefore = chiefInstance.deposits(currentContract);
    uint256 senderGovBalanceBefore = govInstance.balanceOf(e.msg.sender);
    uint256 senderIouBalanceBefore = iouInstance.balanceOf(e.msg.sender);
    uint256 chiefGovBalanceBefore = govInstance.balanceOf(chiefInstance);

    free(e, wad);

    uint256 senderStakeAfter = stake(e.msg.sender);
    uint256 chiefDepositsAfter = chiefInstance.deposits(currentContract);
    uint256 senderGovBalanceAfter = govInstance.balanceOf(e.msg.sender);
    uint256 senderIouBalanceAfter = iouInstance.balanceOf(e.msg.sender);
    uint256 chiefGovBalanceAfter = govInstance.balanceOf(chiefInstance);

    assert(senderStakeAfter == senderStakeBefore - wad, "chief deposit error");
    assert(chiefDepositsAfter == chiefDepositsBefore - wad, "chief deposit error");
    assert(senderGovBalanceAfter == senderGovBalanceBefore + wad, "sender gov balance error");
    assert(senderIouBalanceAfter == senderIouBalanceBefore - wad, "iou balance error");
    assert(chiefGovBalanceAfter == chiefGovBalanceBefore - wad, "chief gov balance error");
}

rule vote_slate(bytes32 newSlate) {
    env e;

    require(currentContract.chief() == chiefInstance);
    require(currentContract.gov() == govInstance);
    require(currentContract.iou() == iouInstance);
    require(chiefInstance.GOV() == govInstance);
    require(chiefInstance.IOU() == iouInstance);

    require(chiefInstance.MAX_YAYS() == 5);

    bytes32 oldSlate = chiefInstance.votes(currentContract);

    uint256 weight = chiefInstance.deposits(currentContract);

    address oldAddr1 = chiefInstance.slates(oldSlate, 0);
    address oldAddr2 = chiefInstance.slates(oldSlate, 1);
    address oldAddr3 = chiefInstance.slates(oldSlate, 2);
    address oldAddr4 = chiefInstance.slates(oldSlate, 3);
    address oldAddr5 = chiefInstance.slates(oldSlate, 4);

    address newAddr1 = chiefInstance.slates(newSlate, 0);
    address newAddr2 = chiefInstance.slates(newSlate, 1);
    address newAddr3 = chiefInstance.slates(newSlate, 2);
    address newAddr4 = chiefInstance.slates(newSlate, 3);
    address newAddr5 = chiefInstance.slates(newSlate, 4);

    uint256 approvalsBeforeOldAddr1 = chiefInstance.approvals(oldAddr1);
    uint256 approvalsBeforeOldAddr2 = chiefInstance.approvals(oldAddr2);
    uint256 approvalsBeforeOldAddr3 = chiefInstance.approvals(oldAddr3);
    uint256 approvalsBeforeOldAddr4 = chiefInstance.approvals(oldAddr4);
    uint256 approvalsBeforeOldAddr5 = chiefInstance.approvals(oldAddr5);

    uint256 approvalsBeforeNewAddr1 = chiefInstance.approvals(newAddr1);
    uint256 approvalsBeforeNewAddr2 = chiefInstance.approvals(newAddr2);
    uint256 approvalsBeforeNewAddr3 = chiefInstance.approvals(newAddr3);
    uint256 approvalsBeforeNewAddr4 = chiefInstance.approvals(newAddr4);
    uint256 approvalsBeforeNewAddr5 = chiefInstance.approvals(newAddr5);

    vote(e, newSlate);

    uint256 approvalsAfterOldAddr1 = chiefInstance.approvals(oldAddr1);
    uint256 approvalsAfterOldAddr2 = chiefInstance.approvals(oldAddr2);
    uint256 approvalsAfterOldAddr3 = chiefInstance.approvals(oldAddr3);
    uint256 approvalsAfterOldAddr4 = chiefInstance.approvals(oldAddr4);
    uint256 approvalsAfterOldAddr5 = chiefInstance.approvals(oldAddr5);

    uint256 approvalsAfterNewAddr1 = chiefInstance.approvals(newAddr1);
    uint256 approvalsAfterNewAddr2 = chiefInstance.approvals(newAddr2);
    uint256 approvalsAfterNewAddr3 = chiefInstance.approvals(newAddr3);
    uint256 approvalsAfterNewAddr4 = chiefInstance.approvals(newAddr4);
    uint256 approvalsAfterNewAddr5 = chiefInstance.approvals(newAddr5);

    assert(chiefInstance.votes(currentContract) == newSlate, "chief vote slate error");

    assert(oldAddr1 != 0 => approvalsAfterOldAddr1 == approvalsBeforeOldAddr1 - weight || approvalsAfterOldAddr1 == approvalsBeforeOldAddr1, "error balance old addr 1");
    assert(oldAddr2 != 0 => approvalsAfterOldAddr2 == approvalsBeforeOldAddr2 - weight || approvalsAfterOldAddr2 == approvalsBeforeOldAddr2, "error balance old addr 2");
    assert(oldAddr3 != 0 => approvalsAfterOldAddr3 == approvalsBeforeOldAddr3 - weight || approvalsAfterOldAddr3 == approvalsBeforeOldAddr3, "error balance old addr 3");
    assert(oldAddr4 != 0 => approvalsAfterOldAddr4 == approvalsBeforeOldAddr4 - weight || approvalsAfterOldAddr4 == approvalsBeforeOldAddr4, "error balance old addr 4");
    assert(oldAddr5 != 0 => approvalsAfterOldAddr5 == approvalsBeforeOldAddr5 - weight || approvalsAfterOldAddr5 == approvalsBeforeOldAddr5, "error balance old addr 5");

    assert(newAddr1 != 0 => approvalsAfterNewAddr1 == approvalsBeforeNewAddr1 + weight || approvalsAfterNewAddr1 == approvalsBeforeNewAddr1, "error balance new addr 1");
    assert(newAddr2 != 0 => approvalsAfterNewAddr2 == approvalsBeforeNewAddr2 + weight || approvalsAfterNewAddr2 == approvalsBeforeNewAddr2, "error balance new addr 2");
    assert(newAddr3 != 0 => approvalsAfterNewAddr3 == approvalsBeforeNewAddr3 + weight || approvalsAfterNewAddr3 == approvalsBeforeNewAddr3, "error balance new addr 3");
    assert(newAddr4 != 0 => approvalsAfterNewAddr4 == approvalsBeforeNewAddr4 + weight || approvalsAfterNewAddr4 == approvalsBeforeNewAddr4, "error balance new addr 4");
    assert(newAddr5 != 0 => approvalsAfterNewAddr5 == approvalsBeforeNewAddr5 + weight || approvalsAfterNewAddr5 == approvalsBeforeNewAddr5, "error balance new addr 5");
}

rule vote_addrs(address[] nYays) {
    env e;

    require(currentContract.chief() == chiefInstance);
    require(currentContract.gov() == govInstance);
    require(currentContract.iou() == iouInstance);
    require(chiefInstance.GOV() == govInstance);
    require(chiefInstance.IOU() == iouInstance);

    require(chiefInstance.MAX_YAYS() == 5);

    bytes32 oldSlate = chiefInstance.votes(currentContract);

    uint256 weight = chiefInstance.deposits(currentContract);

    address oldAddr1 = chiefInstance.slates(oldSlate, 0);
    address oldAddr2 = chiefInstance.slates(oldSlate, 1);
    address oldAddr3 = chiefInstance.slates(oldSlate, 2);
    address oldAddr4 = chiefInstance.slates(oldSlate, 3);
    address oldAddr5 = chiefInstance.slates(oldSlate, 4);

    address newAddr1 = nYays[0];
    address newAddr2 = nYays[1];
    address newAddr3 = nYays[2];
    address newAddr4 = nYays[3];
    address newAddr5 = nYays[4];

    uint256 approvalsBeforeOldAddr1 = chiefInstance.approvals(oldAddr1);
    uint256 approvalsBeforeOldAddr2 = chiefInstance.approvals(oldAddr2);
    uint256 approvalsBeforeOldAddr3 = chiefInstance.approvals(oldAddr3);
    uint256 approvalsBeforeOldAddr4 = chiefInstance.approvals(oldAddr4);
    uint256 approvalsBeforeOldAddr5 = chiefInstance.approvals(oldAddr5);

    uint256 approvalsBeforeNewAddr1 = chiefInstance.approvals(newAddr1);
    uint256 approvalsBeforeNewAddr2 = chiefInstance.approvals(newAddr2);
    uint256 approvalsBeforeNewAddr3 = chiefInstance.approvals(newAddr3);
    uint256 approvalsBeforeNewAddr4 = chiefInstance.approvals(newAddr4);
    uint256 approvalsBeforeNewAddr5 = chiefInstance.approvals(newAddr5);

    vote(e, nYays);

    uint256 approvalsAfterOldAddr1 = chiefInstance.approvals(oldAddr1);
    uint256 approvalsAfterOldAddr2 = chiefInstance.approvals(oldAddr2);
    uint256 approvalsAfterOldAddr3 = chiefInstance.approvals(oldAddr3);
    uint256 approvalsAfterOldAddr4 = chiefInstance.approvals(oldAddr4);
    uint256 approvalsAfterOldAddr5 = chiefInstance.approvals(oldAddr5);

    uint256 approvalsAfterNewAddr1 = chiefInstance.approvals(newAddr1);
    uint256 approvalsAfterNewAddr2 = chiefInstance.approvals(newAddr2);
    uint256 approvalsAfterNewAddr3 = chiefInstance.approvals(newAddr3);
    uint256 approvalsAfterNewAddr4 = chiefInstance.approvals(newAddr4);
    uint256 approvalsAfterNewAddr5 = chiefInstance.approvals(newAddr5);

    assert(chiefInstance.votes(currentContract) == chiefInstance.etch(e, nYays), "chief vote slate error");

    assert(oldAddr1 != 0 => approvalsAfterOldAddr1 == approvalsBeforeOldAddr1 - weight || approvalsAfterOldAddr1 == approvalsBeforeOldAddr1, "error balance old addr 1");
    assert(oldAddr2 != 0 => approvalsAfterOldAddr2 == approvalsBeforeOldAddr2 - weight || approvalsAfterOldAddr2 == approvalsBeforeOldAddr2, "error balance old addr 2");
    assert(oldAddr3 != 0 => approvalsAfterOldAddr3 == approvalsBeforeOldAddr3 - weight || approvalsAfterOldAddr3 == approvalsBeforeOldAddr3, "error balance old addr 3");
    assert(oldAddr4 != 0 => approvalsAfterOldAddr4 == approvalsBeforeOldAddr4 - weight || approvalsAfterOldAddr4 == approvalsBeforeOldAddr4, "error balance old addr 4");
    assert(oldAddr5 != 0 => approvalsAfterOldAddr5 == approvalsBeforeOldAddr5 - weight || approvalsAfterOldAddr5 == approvalsBeforeOldAddr5, "error balance old addr 5");

    assert(newAddr1 != 0 => approvalsAfterNewAddr1 == approvalsBeforeNewAddr1 + weight || approvalsAfterNewAddr1 == approvalsBeforeNewAddr1, "error balance new addr 1");
    assert(newAddr2 != 0 => approvalsAfterNewAddr2 == approvalsBeforeNewAddr2 + weight || approvalsAfterNewAddr2 == approvalsBeforeNewAddr2, "error balance new addr 2");
    assert(newAddr3 != 0 => approvalsAfterNewAddr3 == approvalsBeforeNewAddr3 + weight || approvalsAfterNewAddr3 == approvalsBeforeNewAddr3, "error balance new addr 3");
    assert(newAddr4 != 0 => approvalsAfterNewAddr4 == approvalsBeforeNewAddr4 + weight || approvalsAfterNewAddr4 == approvalsBeforeNewAddr4, "error balance new addr 4");
    assert(newAddr5 != 0 => approvalsAfterNewAddr5 == approvalsBeforeNewAddr5 + weight || approvalsAfterNewAddr5 == approvalsBeforeNewAddr5, "error balance new addr 5");
}
