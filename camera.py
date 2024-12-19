import cv2

def get_camera_frame(cap):
    """Захватывает кадр с камеры."""
    if not cap.isOpened():
        print("Не удалось открыть камеру.")
        return

    ret, frame = cap.read()

    if not ret:
        print("Не удалось захватить кадр.")
        return
    return frame


def display_frame(frame, window_name="Camera Feed"):
    """Отображает кадр в окне."""
    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True
