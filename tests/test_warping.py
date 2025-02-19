import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

import pivuq


def test_warp_skimage():
    frame = np.pad(np.ones((3, 3)), 2)
    U = np.ones((2, *frame.shape))
    coords = np.meshgrid(np.arange(frame.shape[0]), np.arange(frame.shape[1]), indexing="ij")

    assert_array_equal(pivuq.warping.warp_skimage(frame, 0 * U, coords), frame)

    assert_array_equal(pivuq.warping.warp_skimage(frame, U, coords), np.roll(frame, 1, axis=(0, 1)))

    assert_array_equal(
        pivuq.warping.warp_skimage(frame, -1 * U, coords),
        np.roll(frame, -1, axis=(0, 1)),
    )

    assert_array_equal(pivuq.warping.warp_skimage(frame, 10 * U, coords), frame * 0.0)

    assert_array_equal(
        pivuq.warping.warp_skimage(frame, 0.5 * U, coords),
        np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.25, 0.5, 0.5, 0.25, 0.0],
                [0.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0],
                [0.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0],
                [0.0, 0.0, 0.25, 0.5, 0.5, 0.25, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        ),
    )


def test_interpolate_to_pixel():
    U = np.ones((2, 3, 3))
    imshape = (10, 10)
    kind = "linear"

    assert pivuq.warping.interpolate_to_pixel(U, imshape, kind).shape == (2, *imshape)

    assert_allclose(pivuq.warping.interpolate_to_pixel(U, imshape, kind), np.ones((2, *imshape)))


def test_warp():
    frame_a = np.pad(np.ones((3, 3)), 2)
    frame_b = np.roll(frame_a, 1, axis=(0, 1))

    # Test all orders
    warped_frame_a, warped_frame_b = pivuq.warp(
        (frame_a, frame_b),
        np.ones((2, 2, 2)),
        nsteps=1,
        order=1,
    )
    assert_allclose(warped_frame_a, warped_frame_b)

    # warped_frame_a, warped_frame_b = pivuq.warp(
    #    (frame_a, frame_b),
    #    np.ones((2, 2, 2)),
    #    nsteps=1,
    #    order=2,
    # )
    # assert_allclose(warped_frame_a, warped_frame_b)

    warped_frame_a, warped_frame_b = pivuq.warp(
        (frame_a, frame_b),
        np.ones((2, 2, 2)),
        nsteps=1,
        order=3,
    )
    assert_allclose(warped_frame_a, warped_frame_b)

    # Test forward and backward
    warped_frame_a, warped_frame_b = pivuq.warp(
        (frame_a, frame_b),
        np.ones((2, 2, 2)),
        direction="forward",
        nsteps=1,
        order=1,
    )
    assert_allclose(warped_frame_a, warped_frame_b)

    warped_frame_a, warped_frame_b = pivuq.warp(
        (frame_a, frame_b),
        np.ones((2, 2, 2)),
        direction="backward",
        nsteps=1,
        order=1,
    )
    assert_allclose(warped_frame_a, warped_frame_b)
