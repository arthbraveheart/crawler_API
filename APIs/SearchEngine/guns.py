# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:32:35 2024

@author: ArthurRodrigues
"""

import numpy as np


class Guns:
    
    def Mrot(self,v, theta):
        n = v.shape[0]
        M = np.eye(n)

        for c in range(n - 2):
            for r in range(n - 1, c, -1):
                t = np.arctan2(v[r, c], v[r - 1, c])
                R = np.eye(n)
                cos_t = np.cos(t)
                sin_t = np.sin(t)
                R[[r, r - 1], [r, r - 1]] = [cos_t -sin_t, sin_t * cos_t]
                v = R @ v
                M = R @ M

        R = np.eye(n)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        R[[n - 1, n - 2], [n - 1, n - 2]] = np.array([cos_theta -sin_theta, sin_theta * cos_theta])
        M = np.linalg.inv(M) @ R @ M

        return M
        
    def rotate_to(self, u, v):
        """
        Finds the vector k such that norm(u_proj + k) = norm(u),
        where u_proj is the projection of u onto v, and k is in the same direction as v and u_proj.

        Parameters:
        u (np.array): Vector u
        v (np.array): Vector v

        Returns:
        np.array: Vector k
        """
        # Ensure inputs are numpy arrays
        u = np.array(u)
        v = np.array(v)

        # Compute the projection of u onto v
        beta = np.dot(u, v) / np.dot(v, v)
        u_proj = beta * v

        # Compute norms
        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)

        # Compute gamma
        gamma = norm_u / norm_v

        # Compute the two possible solutions for k
        k1 = (gamma - beta) * v
        #k2 = (-gamma - beta) * v

        # Choose k1 as the preferred solution (same direction assumption)
        # If k2 is preferred, use k2 instead
        k = k1

        u = u_proj + k 
        
        return u    
