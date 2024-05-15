import torch


class NextItemMetric(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.reset()

    def update(self, mask, target_timestamps, target_labels,
               predicted_timestamps, predicted_labels_logits):
        """Update metrics with new data.

        Args:
            mask: Valid targets and predictions mask with shape (B, L).
            target_timestamps: Valid target timestamps with shape (B, L).
            target_labels: True labels with shape (B, L).
            predicted_timestamps: Predicted timestamps with shape (B, L).
            predicted_labels_logits: Predicted class logits with shape (B, L, C).
        """
        predictions = predicted_labels_logits.argmax(2)  # (B, L).
        is_correct = predictions == target_labels  # (B, L).
        is_correct = is_correct.masked_select(mask)  # (V).
        ae = (target_timestamps - predicted_timestamps).abs()  # (B, L).
        ae = ae.masked_select(mask)  # (V).
        self._ae_sums.append(ae.float().mean().cpu() * ae.numel())
        self._n_correct_labels += is_correct.sum().item()
        self._n_labels += is_correct.numel()

    def reset(self):
        self._ae_sums = []
        self._n_correct_labels = 0
        self._n_labels = 0

    def compute(self):
        return {
            "next-item-mae": torch.stack(self._ae_sums).sum() / self._n_labels,
            "next-item-accuracy": self._n_correct_labels / self._n_labels
        }
