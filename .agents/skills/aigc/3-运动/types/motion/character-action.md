# Type Package: character-action

适用于人物或角色动作、身体部位动作和状态迁移。

## Motion Signals

- 移动：走、跑、冲、退、靠近、远离、绕过、跨过、进入、离开。
- 姿态：站起、坐下、跪下、倒下、转身、侧身、俯身、抬头、低头。
- 手部：伸手、抓住、松开、推、拉、递、接、按住、挡开。
- 关系：贴近、避开、拦住、追随、让路、扶住、被带动。

## Handling Bias

- 先锁 motion_subject，再从 `group_reference_profile` 继承或选择 reference_frame。
- 对身体部位动作，主体可以是角色的手、肩、视线、重心或脚步，但 final_state 必须回到角色整体状态。
- 多人动作中只让真正移动的角色成为主运动者；其他人写成维持、反应或让位。
