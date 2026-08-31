import asyncio

from prompt_toolkit import PromptSession
from agent import agent, MODEL_NAME, api_call_log
from pydantic_graph import End
from pydantic_ai import Agent

from ui.commands import(
    COMMANDS,
    SessionState,
    console,
    print_agent_steps,
    print_part,
    print_divider,
    print_welcome_banner,
)
# promptSession 比内置 input() 好用：支持左右移动光标编辑，还会记住本次运行的输入历史，上下方向键可以翻
prompt_session = PromptSession()

def read_user_input():
    """
    打印上横线并读一行用户输入；回车后再补充一条下横线，让输入在滚动历史里保持上下边界。
    返回 None 表示用户希望退出（ctrl-C / ctrl-D）。
    """
    print_divider()
    try:
        user_input = prompt_session.prompt("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    print_divider()
    return user_input    

def hand_command(user_input, state):
    """
    处理以 / 开头的命令。
    返回 'pass'：不是命令，主循环继续往下走交给 agent；
    返回 'continue'：命令已处理，主循环跳到下一轮；
    返回 'break'：命令要求退出主循环。
    """
    if not user_input.startswith("/"):
        return "pass"
    cmd_name = user_input[1:].split()[0]
    command = COMMANDS.get(cmd_name)
    if command is None:
        console.print(f"未知命令：/{cmd_name}，输入 /help 查看可用命令\n")
    return "continue" if command.handler(state) else "break"

def apply_result(state, result):
    """
    跑完一轮 Agent 后，把结果同步到 SessionState 并显示增加中间过程。
    """
    state.history = result.all_messages()
    usage = result.usage
    state.input_tokens += usage.input_tokens
    state.output_tokens += usage.output_tokens
    state.last_api_calls = list(api_call_log)
    #result.new_messages() 直接拿到本轮新增的message，不需要手动偏移
    print_agent_steps(result.new_messages())

async def run_agent_loop(user_input, state):
    """
    展开 agent.run_sync()，逐节点驱动 Agent 循环，每步实时打印。
    """
    api_call_log.clear()
    async with agent.iter(user_input, message_history=state.history) as run:
        node = run.next_node
        while not isinstance(node, End):
            node = await run.next(node)
            if Agent.is_call_tools_node(node):
                for part in node.model_response.parts:
                    print_part(part)
            elif Agent.is_model_request_node(node):
                for part in node.request.parts:
                    if part.part_kind == "tool-return":
                        print_part(part)
    apply_result(state, run.result)
    console.print()                            

def main():
    state = SessionState(model_name=MODEL_NAME)
    print_welcome_banner("My Claude Code Agent")

    # agent loop
    while True:
        #读用户输入
        user_input = read_user_input()
        if user_input is None:
            break
        if not user_input:
            continue
        # 处理 / 开头的命令
        action = hand_command(user_input, state)
        if action == "break":
            break
        if action == "continue":
            continue


        try:
            asyncio.run(run_agent_loop(user_input, state))
        except KeyboardInterrupt:
            console.print("\n[bold yellow]已中断[/]\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ {type(e).__name__}: {e}[/]\n")

        # 核心 Agent 循环：自己驱动节点流转，实时打印每一步
        #asyncio.run(run_agent_loop(user_input, state))
        # 核心 Agent 循环：清空收集 buffer，跑一轮，把结果应用到 state
        #api_call_log.clear()
        #result = agent.run_sync(user_input, message_history = state.history)
        #apply_result(state, result)

if __name__ == "__main__":
    main()