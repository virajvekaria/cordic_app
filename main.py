import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow

def cordic_one_iteration(x, y, angle, target, i):
    if(angle == target):
       return x, y, angle
    d = 1
    if(angle>target):
        d = -1

    x_new = (x - (d*(2.0**(-i))*y))
    y_new = ((d*(2.0**(-i))*x) + y)
    angle_new = angle+ (d*(np.arctan(2**(-i))))
    return x_new, y_new, angle_new

def reset():
    st.session_state.x_vals = 1
    st.session_state.y_vals = 0
    st.session_state.angles = 0
    st.session_state.step = 0

def main():
    st.title("CORDIC Rotation Visualization")

    angle_deg = st.slider("Rotation Angle (degrees):", 0.00, 90.00, 60.00,on_change=reset, step = 0.01)
    angle = angle_deg*np.pi/180
    x_init, y_init = 1, 0
    k = 0.6072529350088812561694

    st.session_state.x_vals = st.session_state.get("x_vals", float(x_init))
    st.session_state.y_vals = st.session_state.get("y_vals", float(y_init))
    st.session_state.angles = st.session_state.get("angles", 0)
    st.session_state.step = st.session_state.get("step", 0)

    # if st.button("Reset"):
    #     st.session_state.x_vals = x_init
    #     st.session_state.y_vals = y_init
    #     st.session_state.angles = 0
    #     st.session_state.step = 0

    if "param_history" not in st.session_state:
        st.session_state.param_history = []

    if st.button("Next Iteration"):
        a, b, c = cordic_one_iteration(st.session_state.x_vals, st.session_state.y_vals, st.session_state.angles, angle, st.session_state.step)
        st.session_state.x_vals = a
        st.session_state.y_vals = b
        st.session_state.angles = c
        st.session_state.step += 1
        st.session_state.param_history.append((st.session_state.x_vals, st.session_state.y_vals, st.session_state.angles))

    # Print Cosine and Sine values
    st.write(f"Values of Sine and Cosine after {st.session_state.step} steps:")
    if(st.session_state.step == 0):
        st.write(f"sin({angle_deg}) = {st.session_state.y_vals:.5f}")
        st.write(f"cos({angle_deg}) = {st.session_state.x_vals:.5f}")
    else:
        st.write(f"sin({angle_deg}) = {(st.session_state.y_vals*k):.5f}")
        st.write(f"cos({angle_deg}) = {(st.session_state.x_vals*k):.5f}")


    # Plot the CORDIC path
    fig, ax = plt.subplots(figsize=(8, 8))

    # Add the initial and final vectors as arrows
    ax.plot(0, 0, "k", marker = ".", markersize = 15)
    ax.add_patch(FancyArrow(0, 0, 1, 0, color='green', width=0.02, label='Initial Vector'))
    if(st.session_state.step == 0):
        ax.add_patch(FancyArrow(0, 0, st.session_state.x_vals, st.session_state.y_vals, color='red', width=0.02, label='Current Vector'))
    else:
        ax.add_patch(FancyArrow(0, 0, k*st.session_state.x_vals, k*st.session_state.y_vals, color='red', width=0.02, label='Current Vector'))
    ax.add_patch(FancyArrow(0, 0, np.cos(angle), np.sin(angle), color='blue', width=0.02, label='Current Vector'))

    # Plot a circle of radius 1
    circle = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='dashed', label='Reference circle')
    ax.add_patch(circle)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()

    st.pyplot(fig)

if __name__ == "__main__":
    main()
