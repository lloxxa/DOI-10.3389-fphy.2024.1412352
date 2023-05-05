% pillar

figure()
colorbar()
hold on
nfiles=227;
cmap=colormap(parula);
integrals= 1:nfiles;
peakstrain=1:nfiles;
for i=1:nfiles
    if mod(i,4)==3             %i==4 || i == 8 || i==12 || i==16 ||i==20 ||i==24
        i = i;
        a=importdata(strcat('Eco_P4_FN3_v_3_onespeed_Interval_',int2str(i),'.csv'));

   

    end
z=a.data(:,3);
b=baseline(a.data(:,2), 20);
f=a.data(:,2);

z_0=z (  find(abs(f(1:232))==min(abs(f(1:232))))  );
z_0=z_0(1);
z=z-z_0;

  %  b=importdata(strcat('cup_',int2str(i),'_ret.csv'));
  %  t=b.data(:,3);
   % g=b.data(:,5);
    

    
%     plot(t, g,'DisplayName', int2str(i), ...
%         'Color', colorn(i, nfiles, cmap));
    plot(z, f,'DisplayName', int2str(i), ...
        'Color', colorn(i, nfiles, cmap));
    xlabel('Strain (mm)', 'FontSize', 14);
    ylabel('Force (N)', 'FontSize', 14);
    title('Repeated array measurements', 'FontSize', 14);

    integrals(i)=-integrate(z,f);
    
    % get the baseline
    % find z-value of intersection = point of contact
    % integrate all f < baseline
    grad=gradient(f);
    maxgrad_idx=find(grad==max(grad));
    peakstrain(i)=z(maxgrad_idx(1));
    
  
    
%savefig(g);
figure()
plot(sort(integrals(1:170)));
xlabel('Measurement', 'FontSize', 14);
ylabel('Force (N)', 'FontSize', 14);
title('Array measurements throughout the experiments', 'FontSize', 14);


end
colorbar();
caxis([1 nfiles]);
f=figure();
histogram(integrals, 40);
%savefig(f);
xlim([0, 1500]);
xlabel('Integral (mN/mm)', 'FontSize', 14);
ylabel('Bin Count', 'FontSize', 14);
title('Histogram of Integrals', 'FontSize', 14);
% 
% 
% g=figure();
% histogram(peakstrain, 40);
% xlim([0, 100]);
% xlabel('Peakstrain (mm)', 'FontSize', 14);
% ylabel('Bin Count', 'FontSize', 14);
% title('Histogram of Peakstrain', 'FontSize', 14);


function sum_f=integrate(z,f)
    dz=z(end)/length(f(find(z==0):end));
    sum_f = sum( f(find(z==0):end) ) * dz;
end

function b=baseline(f, ntail)
    b=mean( f( length(f)-ntail:length(f)  ) );
end

% let's go functions
function c=colorn(i, ncolors, cmap)
    n=floor(256/ncolors*i);
    c=cmap(n,:);
end

