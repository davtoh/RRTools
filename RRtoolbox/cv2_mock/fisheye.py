# encoding: utf-8
# module cv2.fisheye
# from /home/davtoh/anaconda3/envs/rrtools/lib/python3.5/site-packages/cv2.cpython-35m-x86_64-linux-gnu.so
# by generator 1.144
# no doc
# no imports

# Variables with simple values

CALIB_CHECK_COND = 4

CALIB_FIX_INTRINSIC = 256
CALIB_FIX_K1 = 16
CALIB_FIX_K2 = 32
CALIB_FIX_K3 = 64
CALIB_FIX_K4 = 128

CALIB_FIX_PRINCIPAL_POINT = 512

CALIB_FIX_SKEW = 8

CALIB_RECOMPUTE_EXTRINSIC = 2

CALIB_USE_INTRINSIC_GUESS = 1

__loader__ = None

__spec__ = None

# functions


# real signature unknown; restored from __doc__
def calibrate(objectPoints, imagePoints, image_size, K, D, rvecs=None, tvecs=None, flags=None, criteria=None):
    """ calibrate(objectPoints, imagePoints, image_size, K, D[, rvecs[, tvecs[, flags[, criteria]]]]) -> retval, K, D, rvecs, tvecs """
    pass


# real signature unknown; restored from __doc__
def distortPoints(undistorted, K, D, distorted=None, alpha=None):
    """ distortPoints(undistorted, K, D[, distorted[, alpha]]) -> distorted """
    pass


# real signature unknown; restored from __doc__
def estimateNewCameraMatrixForUndistortRectify(K, D, image_size, R, P=None, balance=None, new_size=None, fov_scale=None):
    """ estimateNewCameraMatrixForUndistortRectify(K, D, image_size, R[, P[, balance[, new_size[, fov_scale]]]]) -> P """
    pass


# real signature unknown; restored from __doc__
def initUndistortRectifyMap(K, D, R, P, size, m1type, map1=None, map2=None):
    """ initUndistortRectifyMap(K, D, R, P, size, m1type[, map1[, map2]]) -> map1, map2 """
    pass


# real signature unknown; restored from __doc__
def projectPoints(objectPoints, rvec, tvec, K, D, imagePoints=None, alpha=None, jacobian=None):
    """ projectPoints(objectPoints, rvec, tvec, K, D[, imagePoints[, alpha[, jacobian]]]) -> imagePoints, jacobian """
    pass


# real signature unknown; restored from __doc__
def stereoCalibrate(objectPoints, imagePoints1, imagePoints2, K1, D1, K2, D2, imageSize, R=None, T=None, flags=None, criteria=None):
    """ stereoCalibrate(objectPoints, imagePoints1, imagePoints2, K1, D1, K2, D2, imageSize[, R[, T[, flags[, criteria]]]]) -> retval, K1, D1, K2, D2, R, T """
    pass


# real signature unknown; restored from __doc__
def stereoRectify(K1, D1, K2, D2, imageSize, R, tvec, flags, R1=None, R2=None, P1=None, P2=None, Q=None, newImageSize=None, balance=None, fov_scale=None):
    """ stereoRectify(K1, D1, K2, D2, imageSize, R, tvec, flags[, R1[, R2[, P1[, P2[, Q[, newImageSize[, balance[, fov_scale]]]]]]]]) -> R1, R2, P1, P2, Q """
    pass


# real signature unknown; restored from __doc__
def undistortImage(distorted, K, D, undistorted=None, Knew=None, new_size=None):
    """ undistortImage(distorted, K, D[, undistorted[, Knew[, new_size]]]) -> undistorted """
    pass


# real signature unknown; restored from __doc__
def undistortPoints(distorted, K, D, undistorted=None, R=None, P=None):
    """ undistortPoints(distorted, K, D[, undistorted[, R[, P]]]) -> undistorted """
    pass

# no classes
