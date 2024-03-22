import folder_paths
import torch, uuid
import os, sys, shutil
from .utils.preprocess import CropAndExtract
from .test_audio2coeff import Audio2Coeff  
from .facerender.animate import AnimateFromCoeff
from .generate_batch import get_data
from .generate_facerender_batch import get_facerender_data

from .utils.preprocess_two import CropAndExtract as CropAndExtractt
from .test_audio2coeff_two import Audio2Coeff as Audio2Coefft
from .facerender.animate_two import AnimateFromCoeff as AnimateFromCoefft
from .generate_batch_two import get_data as get_datat
from .generate_facerender_batch_two import get_facerender_data as get_facerender_datat
from ..third_part.GFPGAN.gfpgan import GFPGANer
from ..third_part.GPEN.gpen_face_enhancer import FaceEnhancement
import warnings

from .utils.init_path import init_path

from pydub import AudioSegment
import numpy as np
from PIL import Image


def mp3_to_wav(mp3_filename,wav_filename,frame_rate):
    mp3_file = AudioSegment.from_file(file=mp3_filename)
    mp3_file.set_frame_rate(frame_rate).export(wav_filename,format="wav")


class SadTalker():

    def __init__(self, checkpoint_path='checkpoints', config_path='py/src/config', lazy_load=False):

        if torch.cuda.is_available() :
            device = "cuda"
        else:
            device = "cpu"
        
        self.device = device

        os.environ['TORCH_HOME']= checkpoint_path

        self.checkpoint_path = checkpoint_path
        self.config_path = os.path.join(folder_paths.base_path,config_path)
      
    def run_video_2_video(self,pic_path, audio_path,enhancer='lip',batch_size=1,
        use_DAIN=False,remove_duplicates=False,dian_output='dian_output',time_step=0.5,result_dir='./results/'):
        path_of_lm_croper = os.path.join(self.checkpoint_path, 'shape_predictor_68_face_landmarks.dat')
        path_of_net_recon_model = os.path.join(self.checkpoint_path, 'epoch_20.pth')
        dir_of_BFM_fitting = os.path.join(self.checkpoint_path, 'BFM_Fitting')
        wav2lip_checkpoint = os.path.join(self.checkpoint_path, 'wav2lip.pth')

        audio2pose_checkpoint = os.path.join(self.checkpoint_path, 'auido2pose_00140-model.pth')
        audio2pose_yaml_path = os.path.join(self.config_path, 'auido2pose.yaml')

        audio2exp_checkpoint = os.path.join(self.checkpoint_path, 'auido2exp_00300-model.pth')
        audio2exp_yaml_path = os.path.join(self.config_path, 'auido2exp.yaml')

        free_view_checkpoint = os.path.join(self.checkpoint_path, 'facevid2vid_00189-model.pth.tar')

        mapping_checkpoint = os.path.join(self.checkpoint_path, 'mapping_00109-model.pth.tar')
        facerender_yaml_path = os.path.join(self.config_path, 'facerender_still.yaml')

        print("==========",result_dir)
        # init model
        print(path_of_net_recon_model)
        preprocess_model = CropAndExtractt(path_of_lm_croper, path_of_net_recon_model, dir_of_BFM_fitting, self.device)

        print(audio2pose_checkpoint)
        print(audio2exp_checkpoint)
        audio_to_coeff = Audio2Coefft(audio2pose_checkpoint, audio2pose_yaml_path, audio2exp_checkpoint, audio2exp_yaml_path,
                                    wav2lip_checkpoint, self.device)

        print(free_view_checkpoint)
        print(mapping_checkpoint)
        animate_from_coeff = AnimateFromCoefft(free_view_checkpoint, mapping_checkpoint, facerender_yaml_path, self.device)

        restorer_model = GFPGANer(model_path=os.path.join(self.checkpoint_path,'GFPGANv1.3.pth'), upscale=1, arch='clean',
                                channel_multiplier=2, bg_upsampler=None)
        enhancer_model = FaceEnhancement(base_dir=self.checkpoint_path, size=512, model='GPEN-BFR-512', use_sr=False,
                                        sr_model='rrdb_realesrnet_psnr', channel_multiplier=2, narrow=1,device=self.device)

        time_tag = str(uuid.uuid4())
        save_dir = os.path.join(result_dir, time_tag)
        os.makedirs(save_dir, exist_ok=True)
        # crop image and extract 3dmm from image
        first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
        os.makedirs(first_frame_dir, exist_ok=True)
        print('3DMM Extraction for source image')
        first_coeff_path, crop_pic_path, crop_info = preprocess_model.generate(pic_path, first_frame_dir)
        if first_coeff_path is None:
            print("Can't get the coeffs of the input")
            return
        # audio2ceoff
        batch = get_datat(first_coeff_path, audio_path, self.device)
        coeff_path = audio_to_coeff.generate(batch, save_dir)
        # coeff2video
        data = get_facerender_datat(coeff_path, crop_pic_path, first_coeff_path, audio_path, batch_size, self.device)
        tmp_path, new_audio_path, return_path = animate_from_coeff.generate(data, save_dir, pic_path, crop_info,
                                                                            restorer_model, enhancer_model, enhancer)
        torch.cuda.empty_cache()
        if use_DAIN:
            import paddle
            from .dain_model import dain_predictor
            #paddle.device.set_device("gpu") # 把get—device的结果直接复制进去
            paddle.enable_static()
            predictor_dian = dain_predictor.DAINPredictor(dian_output, weight_path=os.path.join(self.checkpoint_path,'DAIN_weight'),
                                                        time_step=time_step,
                                                        remove_duplicates=remove_duplicates)
            frames_path, temp_video_path = predictor_dian.run(tmp_path)
            paddle.disable_static()
            save_path = return_path[:-4] + '_dain.mp4'
            command = r'ffmpeg -y -i "%s" -i "%s" -vcodec copy "%s"' % (temp_video_path, new_audio_path, save_path)
            os.system(command)
        os.remove(tmp_path)
        return return_path

    def run_image_2_video(self, source_image, driven_audio, preprocess='crop', 
        still_mode=False,  use_enhancer=False, batch_size=1, size=256, 
        pose_style = 0, exp_scale=1.0, 
        use_ref_video = False,
        ref_video = None,
        ref_info = None,
        use_idle_mode = False,
        length_of_audio = 0, use_blink=True,
        result_dir='./results/'):

        self.sadtalker_paths = init_path(self.checkpoint_path, self.config_path, size, False, preprocess)
        print(self.sadtalker_paths)
            
        self.audio_to_coeff = Audio2Coeff(self.sadtalker_paths, self.device)
        self.preprocess_model = CropAndExtract(self.sadtalker_paths, self.device)
        self.animate_from_coeff = AnimateFromCoeff(self.sadtalker_paths, self.device)

        time_tag = str(uuid.uuid4())
        save_dir = os.path.join(result_dir, time_tag)
        os.makedirs(save_dir, exist_ok=True)

        input_dir = os.path.join(save_dir, 'input')
        os.makedirs(input_dir, exist_ok=True)

        # print(source_image)
        file = "face_image.png"
        pic_path = os.path.join(input_dir, file) 
        # shutil.move(source_image, input_dir)

        i = 255. * source_image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        img.save(os.path.join(input_dir, file),compress_level=4)

        if driven_audio is not None and os.path.isfile(driven_audio):
            audio_path = os.path.join(input_dir, os.path.basename(driven_audio))  

            #### mp3 to wav
            if '.mp3' in audio_path:
                mp3_to_wav(driven_audio, audio_path.replace('.mp3', '.wav'), 16000)
                audio_path = audio_path.replace('.mp3', '.wav')
            else:
                shutil.move(driven_audio, input_dir)

        elif use_idle_mode: #空闲模式 生成空音频
            audio_path = os.path.join(input_dir, 'idlemode_'+str(length_of_audio)+'.wav') ## generate audio from this new audio_path
            from pydub import AudioSegment
            one_sec_segment = AudioSegment.silent(duration=1000*length_of_audio)  #duration in milliseconds
            one_sec_segment.export(audio_path, format="wav")
        else:
            print(use_ref_video, ref_info)
            assert use_ref_video == True and ref_info == 'all'

        if use_ref_video and ref_info == 'all': # full ref mode
            #提取视频的音频文件
            ref_video_videoname = os.path.basename(ref_video)
            audio_path = os.path.join(save_dir, ref_video_videoname+'.wav')
            print('new audiopath:',audio_path)
            # if ref_video contains audio, set the audio from ref_video.
            cmd = r"ffmpeg -y -hide_banner -loglevel error -i %s %s"%(ref_video, audio_path)
            os.system(cmd)        

        os.makedirs(save_dir, exist_ok=True)
        
        #crop image and extract 3dmm from image #裁剪图像并从图像中提取3dmm
        first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
        os.makedirs(first_frame_dir, exist_ok=True)
        first_coeff_path, crop_pic_path, crop_info = self.preprocess_model.generate(pic_path, first_frame_dir, preprocess, True, size)
        
        if first_coeff_path is None:
            raise AttributeError("No face is detected")

        if use_ref_video:
            print('using ref video for genreation')
            #使用ref视频进行生成
            ref_video_videoname = os.path.splitext(os.path.split(ref_video)[-1])[0]
            ref_video_frame_dir = os.path.join(save_dir, ref_video_videoname)
            os.makedirs(ref_video_frame_dir, exist_ok=True)
            print('3DMM Extraction for the reference video providing pose')
            ref_video_coeff_path, _, _ =  self.preprocess_model.generate(ref_video, ref_video_frame_dir, preprocess, source_image_flag=False)
        else:
            ref_video_coeff_path = None

        if use_ref_video:
            if ref_info == 'pose':
                ref_pose_coeff_path = ref_video_coeff_path
                ref_eyeblink_coeff_path = None
            elif ref_info == 'blink':
                ref_pose_coeff_path = None
                ref_eyeblink_coeff_path = ref_video_coeff_path
            elif ref_info == 'pose+blink':
                ref_pose_coeff_path = ref_video_coeff_path
                ref_eyeblink_coeff_path = ref_video_coeff_path
            elif ref_info == 'all':            
                ref_pose_coeff_path = None
                ref_eyeblink_coeff_path = None
            else:
                raise('error in refinfo')
        else:
            ref_pose_coeff_path = None
            ref_eyeblink_coeff_path = None

        #audio2ceoff
        if use_ref_video and ref_info == 'all':
            coeff_path = ref_video_coeff_path # self.audio_to_coeff.generate(batch, save_dir, pose_style, ref_pose_coeff_path)
        else:
            batch = get_data(first_coeff_path, audio_path, self.device, ref_eyeblink_coeff_path=ref_eyeblink_coeff_path, still=still_mode, idlemode=use_idle_mode, length_of_audio=length_of_audio, use_blink=use_blink) # longer audio?
            coeff_path = self.audio_to_coeff.generate(batch, save_dir, pose_style, ref_pose_coeff_path)

        #coeff2video
        data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path, batch_size, still_mode=still_mode, preprocess=preprocess, size=size, expression_scale = exp_scale)
        return_path = self.animate_from_coeff.generate(data, save_dir,  pic_path, crop_info, enhancer='gfpgan' if use_enhancer else None, preprocess=preprocess, img_size=size)
        video_name = data['video_name']
        print(f'The generated video is named {video_name} in {save_dir}')

        del self.preprocess_model
        del self.audio_to_coeff
        del self.animate_from_coeff

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            
        import gc; gc.collect()
        
        return return_path

    