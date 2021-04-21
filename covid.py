import torchvision
import torch
import numpy as np
import torchvision.transforms as T
from PIL import Image
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

def get_mask_rcnn_model(num_classes = 2, device = None):
    mrcnn_load_path = '/home/healthcare/Banu/LungSegmentation/REDRCNN/MASK RCNN/lung_maskrcnn_albumentations.pt'
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    # Add Object detection branch
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # Add Mask branch
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)
    
    # Load Model
    model.to(device)  
    model.load_state_dict(torch.load(mrcnn_load_path))
    return model

def inference(sample_img_path, save_path, device=torch.device('cuda:2'), mask_th=0.6):
    # Load Image
    ct_img = np.array(Image.open(sample_img_path).convert('RGB'))
    ct_tensor = T.ToTensor()(ct_img)

    # Load Model
    classes = ['Background', 'Lung']
    model = get_mask_rcnn_model(len(classes), device)
    model.eval()

    # Inference
    with torch.no_grad():
        # pass image through the model
        sample_out = model([ct_tensor.to(device)])

        # Extract releevant infomation from model 
        scores = sample_out[0]['scores'].detach().cpu().numpy()
        pos_idx = scores>=0.5
        scores = scores[pos_idx]
        boxes = sample_out[0]['boxes'].detach().cpu().numpy()[pos_idx]
        labels = sample_out[0]['labels'].detach().cpu().numpy()[pos_idx]
        masks = sample_out[0]['masks'].detach().cpu().numpy()[pos_idx]
        sample_boxes = []
        sample_labels = []
        sample_masks = []

        predicted_mask = torch.zeros(ct_tensor.shape[1:]) # contains all the lung region
        ## No distinction between left and right lung
        idx = np.argsort(scores)
    #     print(len(idx), idx.shape)
        if len(idx) == 1:
            sample_masks.append(masks[idx[-1]] >= mask_th)
            combined_mask += masks_torch[idx[-1]].squeeze()
            sample_boxes.append(boxes[idx[-1]])
            sample_labels.append(labels[idx[-1]])
        elif len(idx) >= 2:
            sample_masks.append(masks[idx[-1]] >= mask_th)
            sample_masks.append(masks[idx[-2]] >= mask_th)
            sample_boxes.append(boxes[idx[-1]])
            sample_boxes.append(boxes[idx[-2]])
            sample_labels.extend(labels[idx[-2:]])
            
        for mask in sample_masks:
            predicted_mask += mask
        
        # Save result
        out_pil = Image.fromarray(predicted_mask.squeeze().numpy()*255).convert('L')
        out_pil.save(save_path)
        return predicted_mask

if __name__ == "__main__":
    sample_img_path = "/data/healthcare/Banu/COVID-19/Radiopaedia-CoronacasesCT/5FoldCV/Fold_0/CT/coronacases_002_080.png"
    save_path = '/home/healthcare/Banu/LungSegmentation/REDRCNN/repo/results/others/temp.png'
    out = inference(sample_img_path, save_path)
