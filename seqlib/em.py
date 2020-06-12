'''
Expectation maximization algorithm
modified from SQUAREM (https://github.com/cran/SQUAREM)
'''

import numpy as np
import warnings


def squarem(p0, func, *args, tol=1e-8, maxiter=1500, positive_flag=True,
            **kargs):
    kr = 1
    stepmin = 1
    stepmax0 = 1
    stepmax = 1
    mstep = 4
    n_iter = 0
    while n_iter < maxiter:
        p1 = func(p0, *args, **kargs)
        n_iter += 1
        if np.isnan(p1).any():
            break
        r1 = p1 - p0
        sqr1 = np.sqrt(np.dot(r1, r1))
        if sqr1 <= tol:
            p0 = p1
            break
        p2 = func(p1, *args, **kargs)
        n_iter += 1
        if np.isnan(p2).any():
            break
        r2 = p2 - p1
        sqr2 = np.sqrt(np.dot(r2, r2))
        if sqr2 <= tol:
            p0 = p2
            break
        v = r2 - r1
        sqv = np.sqrt(np.dot(v, v))
        alpha = sqr1 / sqv
        alpha = max(stepmin, min(stepmax, alpha))
        pnew = p0 + 2 * alpha * r1 + alpha**2 * v
        if positive_flag:
            # ! pnew should be positive
            pnew[pnew < 0] = 0
        if abs(alpha - 1) > 0.01:
            ptmp = func(pnew, *args, **kargs)
            n_iter += 1
            if np.isnan(ptmp).any():
                pnew = p2
                if alpha == stepmax:
                    stepmax = max(stepmax0, stepmax / mstep)
                    alpha = 1
            else:
                p_res = ptmp - pnew
                res = np.sqrt(np.dot(p_res, p_res))
                parnorm = np.sqrt(np.dot(p2, p2) / len(p2))
                kres = kr * (1 + parnorm) + sqr2
                pnew = ptmp if res <= kres else p2
                if res > kres:
                    if alpha == stepmax:
                        stepmax = max(stepmax0, stepmax / mstep)
                        alpha = 1
        if alpha == stepmax:
            stepmax = mstep * stepmax
        if stepmin < 0 and alpha == stepmin:
            stepmin = mstep * stepmin
        p0 = pnew
    else:
        warnings.warn('EM did not converge with {} iterations!'.format(n_iter))
    return p0
