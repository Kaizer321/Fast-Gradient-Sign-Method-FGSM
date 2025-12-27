import torch
import torch.nn.functional as F

class Attack:
    def __init__(self, model, device):
        self.model = model
        self.device = device

    def fgsm(self, image, epsilon, data_grad):
        """
        FGSM attack function.
        
        Args:
            image: Original image
            epsilon: Perturbation magnitude
            data_grad: Gradient of the loss w.r.t the input image
            
        Returns:
            Perturbed image
        """
        # Collect the element-wise sign of the data gradient
        sign_data_grad = data_grad.sign()
        
        # Create the perturbed image by adjusting each pixel of the input image
        perturbed_image = image + epsilon * sign_data_grad
        
        # Adding clipping to maintain [0,1] range (assuming data is normalized or in standard range)
        # Note: If the model uses specific normalization, this might need adjustment, 
        # but for standard attacks we usually clip.
        perturbed_image = torch.clamp(perturbed_image, 0, 1)
        
        return perturbed_image

    def perform_attack(self, image, epsilon, target_class):
        """
        Performs the attack on a single image.
        
        Args:
           image: The input image tensor (1, 1, 28, 28)
           epsilon: The perturbation amount
           target_class: The true label of the image
           
        Returns:
            final_pred: Prediction on the adversarial example
            perturbed_image: The adversarial image
        """
        image = image.to(self.device)
        target = torch.tensor([target_class]).to(self.device).long()
        
        # Set requires_grad attribute of tensor. Important for Attack
        image.requires_grad = True

        # Forward pass the data through the model
        output = self.model(image)
        init_pred = output.max(1, keepdim=True)[1] # get the index of the max log-probability

        # Calculate the loss
        loss = F.nll_loss(output, target)

        # Zero all existing gradients
        self.model.zero_grad()

        # Calculate gradients of model in backward pass
        loss.backward()

        # Collect datagrad
        data_grad = image.grad.data
        
        # Call FGSM Attack
        perturbed_data = self.fgsm(image, epsilon, data_grad)
        
        # Re-classify the perturbed image
        output = self.model(perturbed_data)
        final_pred = output.max(1, keepdim=True)[1]
        
        return init_pred.item(), final_pred.item(), perturbed_data.detach()
