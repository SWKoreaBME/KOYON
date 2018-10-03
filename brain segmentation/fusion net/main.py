from FusionNet import *
from model_utils_sw import *

from random import shuffle
'''
    main.py

    main code for train Fusion Net

    18 / 10 / 3
        (1) path removed, annotations added
'''

# hyperparameters

batch_size = 16
img_size = 256
lr = 0.01
epoch = 200
val_percent = 0.1

# input pipeline
img_dir = '/path/to/img_dir'
mask_dir = '/path/to/mask_dir'

res = split_train_val(img_dir, val_percent=val_percent)

fusion = nn.DataParallel(FusionGenerator(input_nc=1, output_nc=1, ngf=32)).cuda(0)

loss_func = nn.SmoothL1Loss()
optimizer = torch.optim.Adam(fusion.parameters(), lr=lr)

print('batch size      :  {}\n'
      'img size        :  {}\n'
      'learning rate   :  {}\n'
      'epoch           :  {}\n'
      'val percentage  :  {}'.format(batch_size, img_size, lr, epoch, val_percent))

for e in range(epoch):

    def batch(iterable, n):
        # https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
        l = len(iterable)
        shuffle(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

    print('\nepoch {}'.format(e + 1))
    dice_sum = 0
    
    for _, batch in enumerate(batch(iterable=res['train'], n=batch_size)):

        data = BatchSet(batch, img_dir, mask_dir, img_size, cuda=True)
        imgs, labels = data

        for i, (img, label) in enumerate(zip(imgs, labels)):
            img = torch.unsqueeze(img, 0)
            label = torch.unsqueeze(label, 0)

            optimizer.zero_grad()

            x = Variable(img).cuda(0)
            y_ = Variable(label).cuda(0)
            y = fusion.forward(x)

            loss = loss_func(y, y_)
            loss.backward()
            optimizer.step()

            # dice coefficient
            dice_sum += DiceCoefficient(y_, y)

            # print('epoch {} batch {} in batch {}'.format(e, _, i+1))
        print('dice sum -- {}'.format(dice_sum))

        if _ % 50 == 0:
            v_utils.save_image(x[0].cpu().data, "./result/original_image_{}_{}.png".format(e, _))
            v_utils.save_image(y_[0].cpu().data, "./result/label_image_{}_{}.png".format(e, _))
            v_utils.save_image(y[0].cpu().data, "./result/gen_image_{}_{}.png".format(e, _))

        print('{} / {} | loss --- {}  dice --- {}'.format((_+1) * batch_size, len(res['train']), loss, (dice_sum / batch_size)))
        dice_sum = 0

    # print validation dice coefficient
    val_imgs, val_labels = MakeVal(batch_size=len(res['val']), img_size=img_size, train_list=res['val'],
                                   cuda=True, img_dir=img_dir, mask_dir=mask_dir)

    print('\nval dice --- {}'.format(ValidDice(val_imgs, val_labels, fusion)))

torch.save(fusion, "./fusion.pkl")