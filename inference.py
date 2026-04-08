import os
import sys
import json
import traceback
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from vaxgym.environment import VaxGymEnv

def main():
    api_base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
    model_name = os.environ.get("MODEL_NAME", "meta-llama/Meta-Llama-3-70B-Instruct")
    hf_token = os.environ.get("HF_TOKEN")

    if not hf_token:
        # We must emit [END] even on exception per rules
        print("[START] task=vaxguard_nav env=VaxGym-v0 model=" + model_name)
        print("[END] success=false steps=0 rewards=0.00")
        return

    client = OpenAI(api_key=hf_token, base_url=api_base_url)

    env = VaxGymEnv()
    
    steps = 0
    total_reward = 0.0
    task_name = "VaxGuard Thermal Cold-Chain Nav"
    env_name = "VaxGym-v0"

    print(f"[START] task={task_name} env={env_name} model={model_name}")

    success = False
    last_action_error = "null"

    try:
        obs, info = env.reset()
        done = False
        
        while not done and steps < 100:
            prompt = f"Observation: {obs}. Action space: {env.action_space_summary()}. Provide action as valid JSON array of 3 integers: [cooling(0-3), route(0-2), sync(0-1)]."
            
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are an agent operating an environment. Output only valid JSON arrays representing the action."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=20,
                    temperature=0.0
                )
                
                action_text = response.choices[0].message.content.strip()
                action = json.loads(action_text)
                
                obs, reward, terminated, truncated, info = env.step(action)
                
                done = terminated or truncated
                total_reward += reward
                steps += 1
                
                if info.get("delivery_status") == "delivered" and info.get("expiry_status") != "spoiled":
                    success = True
                
                print(f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error=null")
                
            except Exception as e:
                done = True
                last_action_error = str(e).replace('\n', ' ')
                print(f"[STEP] step={steps+1} action=null reward=0.00 done=true error={last_action_error}")
                break

    except Exception as e:
        last_action_error = str(e).replace('\n', ' ')
        
    finally:
        print(f"[END] success={str(success).lower()} steps={steps} rewards={total_reward:.2f}")

if __name__ == "__main__":
    main()
