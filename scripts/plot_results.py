import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    traj_path = "logs/eval_trajectory.csv"
    eff_path = "logs/efficiency_curve.csv"
    
    if not os.path.exists(traj_path) or not os.path.exists(eff_path):
        return
        
    df_traj = pd.read_csv(traj_path)
    
    plt.figure(figsize=(10, 5), dpi=150)
    plt.plot(df_traj['step'], df_traj['temperature'], label='Core Temperature (C)', color='cyan', linewidth=2)
    plt.plot(df_traj['step'], df_traj['ambient'], label='Ambient Temp (C)', color='orange', linewidth=1, alpha=0.5)
    plt.axhline(y=2.0, color='lime', linestyle='--', label='Safe Min (2.0C)')
    plt.axhline(y=8.0, color='red', linestyle='--', label='Safe Max (8.0C)')
        
    plt.title('VaxGym Thermal Stabilization Matrix', fontsize=14)
    plt.xlabel('Timesteps')
    plt.ylabel('Temperature (Celsius)')
    plt.ylim(0.0, max(50.0, df_traj['ambient'].max() + 5))
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    os.makedirs('logs', exist_ok=True)
    plt.savefig('logs/thermal_plot.png', bbox_inches='tight')
    
    df_eff = pd.read_csv(eff_path)
    df_eff['reward_smooth'] = df_eff['episode_reward'].rolling(window=15).mean()
    df_eff['mkt_smooth'] = df_eff['mkt_stability'].rolling(window=15).mean()
    
    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=150)

    color1 = 'tab:red'
    ax1.set_xlabel('Episodes')
    ax1.set_ylabel('Reward', color=color1)
    ax1.plot(df_eff['episode'], df_eff['reward_smooth'], color=color1, linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()  
    color2 = 'tab:blue'
    ax2.set_ylabel('MKT Stability (Celsius)', color=color2)  
    ax2.plot(df_eff['episode'], df_eff['mkt_smooth'], color=color2, linewidth=2, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.title('Convergence Analysis: Reward vs MKT Stability', fontsize=14)
    fig.tight_layout()  
    plt.savefig('logs/mkt_curve.png', bbox_inches='tight')

if __name__ == "__main__":
    main()
